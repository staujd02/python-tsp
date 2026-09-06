/* Hull Cut Workbench -- front end.
   Talks to the local server, draws the plot, and polls a running solve. */

(function () {
  "use strict";

  var SVG_NS = "http://www.w3.org/2000/svg";
  var EXTENT = 1000;               // the coordinate space the generator uses
  var POLL_MS = 250;

  var state = {
    config: null,
    mode: "random",
    points: [],
    result: null,
    job: null,
    suiteJob: null,
    suiteRows: null,
    timer: null,
    clockTimer: null
  };

  var el = {};
  ["status-pill", "status-clock", "controls", "size", "size-readout", "size-hint", "seed",
   "reroll", "clear-points", "seed-points", "custom-count", "strategies", "time-limit",
   "limit-readout", "cross-check", "run", "cancel", "run-hint", "plot", "legend",
   "plot-veil", "veil-text", "metrics", "tour-path", "verdict", "toast", "tab-plot",
   "tab-suite", "panel-plot", "panel-suite", "suite-form", "suite-sizes",
   "suite-strategies", "suite-trials", "suite-seed", "suite-run", "suite-cancel",
   "suite-progress", "suite-bar", "suite-message", "suite-results", "suite-chart",
   "suite-table", "suite-empty", "layer-hulls", "layer-cuts", "layer-check",
   "layer-labels"].forEach(function (id) {
    el[id] = document.getElementById(id);
  });

  var layers = {};
  ["grid", "cut-edges", "hull-rings", "check-tour", "tour", "cities"].forEach(function (name) {
    layers[name] = document.getElementById("layer-" + name);
  });

  // ---------------------------------------------------------------- helpers

  function node(name, attributes, parent) {
    var element = document.createElementNS(SVG_NS, name);
    for (var key in attributes) {
      if (attributes[key] !== null && attributes[key] !== undefined) {
        element.setAttribute(key, attributes[key]);
      }
    }
    if (parent) { parent.appendChild(element); }
    return element;
  }

  function clear(element) {
    while (element.firstChild) { element.removeChild(element.firstChild); }
  }

  function api(path, body) {
    return fetch(path, {
      method: body === undefined ? "GET" : "POST",
      headers: { "Content-Type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body)
    }).then(function (response) {
      return response.json().then(function (payload) {
        if (!response.ok) { throw new Error(payload.error || "Request failed."); }
        return payload;
      });
    });
  }

  var toastTimer = null;
  function toast(message) {
    el.toast.textContent = message;
    el.toast.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.toast.hidden = true; }, 5200);
  }

  function seconds(value) {
    if (value === null || value === undefined) { return "--"; }
    if (value < 0.001) { return "<0.001s"; }
    if (value < 1) { return value.toFixed(3) + "s"; }
    if (value < 60) { return value.toFixed(2) + "s"; }
    return Math.floor(value / 60) + "m " + (value % 60).toFixed(0) + "s";
  }

  function setStatus(text, tone) {
    el["status-pill"].textContent = text;
    el["status-pill"].dataset.tone = tone;
  }

  function startClock() {
    var began = Date.now();
    stopClock();
    el["status-clock"].textContent = "0.0s";
    state.clockTimer = setInterval(function () {
      el["status-clock"].textContent = ((Date.now() - began) / 1000).toFixed(1) + "s";
    }, 100);
  }

  function stopClock(finalText) {
    clearInterval(state.clockTimer);
    state.clockTimer = null;
    if (finalText !== undefined) { el["status-clock"].textContent = finalText; }
  }

  // ---------------------------------------------------------------- plot

  function project(point) {
    // Screen y grows downward; the generator's y grows upward.
    return [point[0], EXTENT - point[1]];
  }

  function byLabel() {
    var index = {};
    state.points.forEach(function (point) { index[point[2]] = point; });
    return index;
  }

  function drawGrid() {
    clear(layers.grid);
    for (var at = 250; at < EXTENT; at += 250) {
      node("line", { x1: at, y1: 0, x2: at, y2: EXTENT, class: "grid-line" }, layers.grid);
      node("line", { x1: 0, y1: at, x2: EXTENT, y2: at, class: "grid-line" }, layers.grid);
    }
    node("rect", { x: 0, y: 0, width: EXTENT, height: EXTENT, class: "plot-frame" }, layers.grid);
  }

  function drawCities(tour) {
    clear(layers.cities);
    var start = tour && tour.length ? tour[0] : null;
    var showLabels = el["layer-labels"].checked;
    state.points.forEach(function (point) {
      var xy = project(point);
      var isStart = point[2] === start;
      node("circle", {
        cx: xy[0], cy: xy[1], r: isStart ? 13 : 10,
        class: "city" + (isStart ? " city--start" : "")
      }, layers.cities);
      if (showLabels) {
        node("text", {
          x: xy[0] + 17, y: xy[1] - 14, class: "city-label"
        }, layers.cities).textContent = point[2];
      }
    });
  }

  function drawCutEdges(pairs) {
    clear(layers["cut-edges"]);
    if (!pairs || !el["layer-cuts"].checked) { return; }
    var index = byLabel();
    pairs.forEach(function (pair) {
      var a = index[pair[0]];
      var b = index[pair[1]];
      if (!a || !b) { return; }
      var pa = project(a);
      var pb = project(b);
      node("line", { x1: pa[0], y1: pa[1], x2: pb[0], y2: pb[1], class: "cut-edge" },
        layers["cut-edges"]);
    });
  }

  function drawHullRings(rings) {
    clear(layers["hull-rings"]);
    if (!rings || !el["layer-hulls"].checked) { return; }
    var index = byLabel();
    rings.forEach(function (ring, depth) {
      if (ring.length < 3) { return; }
      var points = ring.map(function (label) {
        var point = index[label];
        return point ? project(point).join(",") : null;
      }).filter(Boolean);
      node("polygon", {
        points: points.join(" "),
        class: "hull-ring" + (depth > 0 ? " hull-ring--inner" : "")
      }, layers["hull-rings"]);
    });
  }

  function tourPoints(tour) {
    var index = byLabel();
    return tour.map(function (label) {
      var point = index[label];
      return point ? project(point).join(",") : null;
    }).filter(Boolean).join(" ");
  }

  function drawTour(tour, animate) {
    clear(layers.tour);
    if (!tour || tour.length < 2) { return; }
    var line = node("polyline", { points: tourPoints(tour), class: "tour-path" }, layers.tour);
    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!animate || reduced || !line.getTotalLength) { return; }
    var length = line.getTotalLength();
    line.style.strokeDasharray = length;
    line.style.strokeDashoffset = length;
    line.getBoundingClientRect();          // force the start state to apply
    line.style.transition = "stroke-dashoffset 900ms cubic-bezier(.4,0,.2,1)";
    line.style.strokeDashoffset = "0";
  }

  function drawCheckTour(check) {
    clear(layers["check-tour"]);
    if (!check || !check.tour || !el["layer-check"].checked) { return; }
    node("polyline", { points: tourPoints(check.tour), class: "check-path" },
      layers["check-tour"]);
  }

  function renderLegend(result) {
    var items = [
      ["var(--accent)", "solid", "Tour"],
      ["var(--hull)", "solid", "Hull rings"]
    ];
    if (result && result.exclusionPairs && result.exclusionPairs.length) {
      items.push(["var(--cut)", "dashed", "Eliminated edges"]);
    }
    if (el["layer-check"].checked && result && result.crossCheck) {
      items.push(["var(--ink-soft)", "dotted", "Cross-check tour"]);
    }
    clear(el.legend);
    items.forEach(function (item) {
      var span = document.createElement("span");
      var swatch = document.createElement("i");
      swatch.style.borderTopColor = item[0];
      swatch.style.borderTopStyle = item[1];
      span.appendChild(swatch);
      span.appendChild(document.createTextNode(item[2]));
      el.legend.appendChild(span);
    });
  }

  function redraw(animateTour) {
    var result = state.result;
    drawGrid();
    drawCutEdges(result ? result.exclusionPairs : null);
    drawHullRings(result ? result.hullRings : null);
    drawCheckTour(result ? result.crossCheck : null);
    drawTour(result ? result.tour : null, animateTour);
    drawCities(result ? result.tour : null);
    renderLegend(result);
  }

  // ---------------------------------------------------------------- readout

  function metric(term, value, note, wide) {
    var block = document.createElement("div");
    block.className = "metric" + (wide ? " metric--wide" : "");
    var dt = document.createElement("dt");
    dt.textContent = term;
    var dd = document.createElement("dd");
    dd.textContent = value;
    block.appendChild(dt);
    block.appendChild(dd);
    if (note) {
      var small = document.createElement("small");
      small.textContent = note;
      block.appendChild(small);
    }
    return block;
  }

  function renderReadout(result) {
    clear(el.metrics);
    if (!result) { return; }

    var cutPercent = result.totalEdges
      ? Math.round((result.eliminatedEdges / result.totalEdges) * 100) : 0;

    el.metrics.appendChild(metric(
      "Tour length",
      result.tourLength === null ? "no tour" : result.tourLength.toLocaleString(),
      "sum of edge distances"));
    el.metrics.appendChild(metric(
      "Search time", seconds(result.solveSeconds),
      "cuts took " + seconds(result.cutSeconds)));
    el.metrics.appendChild(metric(
      "Augment vectors", result.augmentVectors.toLocaleString(),
      "edges the queue can reach for"));
    el.metrics.appendChild(metric(
      "Edges eliminated",
      result.eliminatedEdges + " / " + result.totalEdges,
      cutPercent + "% of the directed edges"));
    el.metrics.appendChild(metric(
      "Reduced cost",
      result.reducedCost === null ? "--" : result.reducedCost.toLocaleString(),
      "the solver's objective after column zeroing"));
    el.metrics.appendChild(metric("Cities", String(result.size), "seed " + (result.seed === null || result.seed === undefined ? "hand placed" : result.seed)));

    if (result.tour) {
      el["tour-path"].textContent = result.tour.join(" → ");
    } else {
      el["tour-path"].textContent = result.note || "No valid tour was found.";
    }

    renderVerdict(result);
  }

  function renderVerdict(result) {
    var check = result.crossCheck;
    if (!check) { el.verdict.hidden = true; return; }

    var copy = {
      match: ["Cross-check agrees", "Both routes measure " + check.tourLength + "."],
      worse: ["Cross-check found a shorter tour",
        "The workbench tour is " + check.gap + " longer than " + check.tourLength +
        ". With an exact check that means a cut removed an edge the optimum needed."],
      better: ["The solver beat the cross-check",
        "The cross-check is a heuristic, so this is expected rather than alarming."],
      unknown: ["Nothing to compare", "The solver returned no tour."]
    }[check.verdict] || ["Cross-check", ""];

    // A heuristic that merely ties or loses proves nothing on its own.
    if (check.verdict === "match" && check.method === "heuristic") {
      copy = ["Cross-check ties", "2-opt reached the same length. Agreement, not proof."];
    }

    clear(el.verdict);
    el.verdict.dataset.verdict = check.verdict;
    var strong = document.createElement("strong");
    strong.textContent = copy[0];
    var detail = document.createElement("p");
    detail.textContent = copy[1];
    var method = document.createElement("p");
    method.textContent = check.headline + " Took " + seconds(check.seconds) + ".";
    el.verdict.appendChild(strong);
    el.verdict.appendChild(detail);
    el.verdict.appendChild(method);
    el.verdict.hidden = false;
  }

  // ---------------------------------------------------------------- solving

  function selectedStrategy() {
    var checked = el.strategies.querySelector("input:checked");
    return checked ? checked.value : "none";
  }

  function requestBody() {
    var body = {
      strategy: selectedStrategy(),
      crossCheck: el["cross-check"].checked,
      timeLimit: Number(el["time-limit"].value)
    };
    if (state.mode === "custom") {
      body.mode = "custom";
      body.coords = state.points.map(function (point) { return [point[0], point[1]]; });
    } else {
      body.mode = "random";
      body.size = Number(el.size.value);
      body.seed = Number(el.seed.value);
    }
    return body;
  }

  function setRunning(running) {
    el.run.disabled = running;
    el.cancel.disabled = !running;
    el["plot-veil"].hidden = !running;
    el.run.textContent = running ? "Solving" : "Solve";
  }

  function solve(event) {
    if (event) { event.preventDefault(); }
    if (state.mode === "custom" && state.points.length < 3) {
      toast("Place at least three cities first.");
      return;
    }
    setRunning(true);
    setStatus("Searching", "running");
    startClock();
    el["veil-text"].textContent = "Searching " + (state.mode === "custom"
      ? state.points.length : el.size.value) + " cities";

    api("/api/solve", requestBody()).then(function (job) {
      state.job = job.id;
      poll(job.id);
    }).catch(function (error) {
      setRunning(false);
      stopClock("--");
      setStatus("Failed", "failed");
      toast(error.message);
    });
  }

  function poll(jobId) {
    clearTimeout(state.timer);
    state.timer = setTimeout(function () {
      api("/api/job/" + jobId).then(function (job) {
        if (state.job !== jobId) { return; }
        if (job.points) {
          state.points = job.points;
          if (!state.result) { redraw(false); }
        }
        if (job.state === "running") { poll(jobId); return; }
        finishSolve(job);
      }).catch(function (error) {
        setRunning(false);
        stopClock("--");
        setStatus("Failed", "failed");
        toast(error.message);
      });
    }, POLL_MS);
  }

  function finishSolve(job) {
    state.job = null;
    setRunning(false);
    stopClock(seconds(job.elapsed));

    if (job.state !== "done" || !job.result) {
      setStatus(job.state === "cancelled" ? "Cancelled"
        : job.state === "timeout" ? "Timed out" : "Failed",
        job.state === "cancelled" ? "idle" : "failed");
      toast(job.error || "The solve did not finish.");
      return;
    }

    state.result = job.result;
    state.points = job.result.points;
    setStatus(job.result.solved ? "Solved" : "No tour", job.result.solved ? "done" : "failed");
    redraw(true);
    renderReadout(job.result);
    if (!job.result.solved) { toast(job.result.note); }
  }

  function cancel() {
    if (!state.job) { return; }
    api("/api/cancel/" + state.job, {}).catch(function () {});
  }

  // ---------------------------------------------------------------- instance

  function refreshInstance() {
    if (state.mode !== "random") { return; }
    state.result = null;
    renderReadout(null);
    el.verdict.hidden = true;
    el["tour-path"].textContent = "Press Solve to search this instance.";
    api("/api/instance", { mode: "random", size: Number(el.size.value), seed: Number(el.seed.value) })
      .then(function (payload) {
        state.points = payload.points;
        redraw(false);
        setStatus("Ready", "idle");
        stopClock("—");
      }).catch(function (error) { toast(error.message); });
  }

  function plotCoordinates(event) {
    var box = el.plot.getBoundingClientRect();
    var view = el.plot.viewBox.baseVal;
    var x = view.x + ((event.clientX - box.left) / box.width) * view.width;
    var y = view.y + ((event.clientY - box.top) / box.height) * view.height;
    return [Math.round(x), Math.round(EXTENT - y)];
  }

  function relabel() {
    var alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    state.points = state.points.map(function (point, index) {
      return [point[0], point[1], alphabet[index]];
    });
    el["custom-count"].textContent = state.points.length;
  }

  function onPlotClick(event) {
    if (state.mode !== "custom") { return; }
    var at = plotCoordinates(event);
    var hitIndex = -1;
    state.points.forEach(function (point, index) {
      var dx = point[0] - at[0];
      var dy = point[1] - at[1];
      if (Math.sqrt(dx * dx + dy * dy) < 26) { hitIndex = index; }
    });

    if (hitIndex >= 0) {
      state.points.splice(hitIndex, 1);
    } else {
      if (state.points.length >= state.config.maxCities) {
        toast("The solver labels cities A to Z, so " + state.config.maxCities + " is the ceiling.");
        return;
      }
      if (at[0] < 0 || at[1] < 0 || at[0] > EXTENT || at[1] > EXTENT) { return; }
      state.points.push([at[0], at[1], "?"]);
    }
    relabel();
    state.result = null;
    renderReadout(null);
    el.verdict.hidden = true;
    el["tour-path"].textContent = state.points.length < 3
      ? "Place at least three cities."
      : "Press Solve to search this instance.";
    redraw(false);
  }

  function setMode(mode) {
    state.mode = mode;
    document.querySelectorAll("[data-mode-panel]").forEach(function (panel) {
      panel.hidden = panel.dataset.modePanel !== mode;
    });
    el.plot.classList.toggle("is-placing", mode === "custom");
    if (mode === "custom") {
      relabel();
      state.result = null;
      renderReadout(null);
      el.verdict.hidden = true;
      el["tour-path"].textContent = state.points.length < 3
        ? "Place at least three cities."
        : "Press Solve to search this instance.";
      redraw(false);
    } else {
      refreshInstance();
    }
  }

  // ---------------------------------------------------------------- guidance

  // Measured on the reference machine: an uncut solve runs roughly sixfold
  // longer per extra city (10 cities ~5s, 12 cities ~4min).
  function sizeGuidance(size, strategy) {
    if (size <= 9) { return "Well inside a blink."; }
    if (size <= 10) { return "A few seconds with no cuts, well under one with a deep cut."; }
    if (size <= 11) { return "Tens of seconds uncut. Cuts earn their keep here."; }
    if (size <= 12) {
      return strategy === "none"
        ? "Around four minutes with no elimination. Raise the time limit or pick a cut."
        : "Around a minute even with cuts. Watch the time limit.";
    }
    return "Past the practical ceiling for this solver -- expect to hit the time limit.";
  }

  function updateGuidance() {
    var size = Number(el.size.value);
    el["size-readout"].textContent = size;
    el["size-hint"].textContent = sizeGuidance(size, selectedStrategy());
    el["limit-readout"].textContent = el["time-limit"].value + "s";
    var count = state.mode === "custom" ? state.points.length : size;
    el["run-hint"].textContent = count > state.config.bruteForceLimit && el["cross-check"].checked
      ? "Above " + state.config.bruteForceLimit + " cities the cross-check falls back to 2-opt, which bounds the answer but cannot prove it."
      : "The cross-check searches every tour exhaustively at this size.";
  }

  // ---------------------------------------------------------------- suite

  function buildSuiteControls() {
    for (var size = 4; size <= 12; size += 1) {
      var label = document.createElement("label");
      label.className = "chip";
      label.innerHTML = '<input type="checkbox" value="' + size + '"' +
        (size >= 8 && size <= 10 ? " checked" : "") + '><span>' + size + '</span>';
      el["suite-sizes"].appendChild(label);
    }
    state.config.strategies.forEach(function (strategy, index) {
      var label = document.createElement("label");
      label.className = "chip chip--text";
      var input = document.createElement("input");
      input.type = "checkbox";
      input.value = strategy.key;
      input.checked = index === 0 || strategy.key === "windows";
      var span = document.createElement("span");
      span.textContent = strategy.label;
      label.appendChild(input);
      label.appendChild(span);
      el["suite-strategies"].appendChild(label);
    });
  }

  function checkedValues(container) {
    return Array.prototype.slice.call(container.querySelectorAll("input:checked"))
      .map(function (input) { return input.value; });
  }

  function runSuite(event) {
    event.preventDefault();
    var sizes = checkedValues(el["suite-sizes"]).map(Number).sort(function (a, b) { return a - b; });
    var strategies = checkedValues(el["suite-strategies"]);
    if (!sizes.length || !strategies.length) {
      toast("Pick at least one city count and one strategy.");
      return;
    }

    el["suite-run"].disabled = true;
    el["suite-cancel"].disabled = false;
    el["suite-progress"].hidden = false;
    el["suite-empty"].hidden = true;
    el["suite-bar"].style.width = "0%";
    el["suite-message"].textContent = "Starting";
    setStatus("Running suite", "running");
    startClock();

    api("/api/suite", {
      sizes: sizes,
      strategies: strategies,
      trials: Number(el["suite-trials"].value),
      seed: Number(el["suite-seed"].value),
      timeLimit: 0
    }).then(function (job) {
      state.suiteJob = job.id;
      pollSuite(job.id);
    }).catch(function (error) {
      finishSuite(null, error.message);
    });
  }

  function pollSuite(jobId) {
    setTimeout(function () {
      api("/api/job/" + jobId).then(function (job) {
        if (state.suiteJob !== jobId) { return; }
        var progress = job.progress || {};
        if (progress.total) {
          el["suite-bar"].style.width = ((progress.done / progress.total) * 100).toFixed(1) + "%";
        }
        el["suite-message"].textContent = progress.message || "";
        if (job.state === "running") { pollSuite(jobId); return; }
        if (job.state === "done" && job.result) {
          finishSuite(job.result, null);
        } else {
          finishSuite(null, job.error || "The suite did not finish.");
        }
      }).catch(function (error) { finishSuite(null, error.message); });
    }, 300);
  }

  function finishSuite(result, errorMessage) {
    state.suiteJob = null;
    el["suite-run"].disabled = false;
    el["suite-cancel"].disabled = true;
    el["suite-progress"].hidden = true;
    stopClock();

    if (errorMessage) {
      setStatus("Failed", "failed");
      toast(errorMessage);
      if (!state.suiteRows) { el["suite-empty"].hidden = false; }
      return;
    }
    setStatus("Suite complete", "done");
    state.suiteRows = result.rows;
    renderSuite(result.rows);
  }

  function renderSuite(rows) {
    el["suite-results"].hidden = false;
    el["suite-empty"].hidden = true;
    renderSuiteChart(rows);
    renderSuiteTable(rows);
  }

  function renderSuiteChart(rows) {
    clear(el["suite-chart"]);
    var sizes = [];
    rows.forEach(function (row) {
      if (sizes.indexOf(row.size) === -1) { sizes.push(row.size); }
    });

    sizes.forEach(function (size) {
      var group = rows.filter(function (row) { return row.size === size; });
      var slowest = Math.max.apply(null, group.map(function (row) { return row.mean; }));
      var fastest = Math.min.apply(null, group.map(function (row) { return row.mean; }));

      var wrapper = document.createElement("div");
      wrapper.className = "chart__group";
      var title = document.createElement("p");
      title.className = "chart__title";
      title.textContent = size + " cities · mean search time over " + group[0].trials +
        (group[0].trials === 1 ? " trial" : " trials");
      wrapper.appendChild(title);

      group.forEach(function (row) {
        var bar = document.createElement("div");
        bar.className = "bar" + (row.mean === fastest ? " bar--best" : "");
        var label = document.createElement("span");
        label.className = "bar__label";
        label.textContent = row.label;
        var track = document.createElement("span");
        track.className = "bar__track";
        var fill = document.createElement("span");
        fill.className = "bar__fill";
        fill.style.width = slowest > 0 ? ((row.mean / slowest) * 100).toFixed(1) + "%" : "0%";
        track.appendChild(fill);
        var value = document.createElement("span");
        value.className = "bar__value";
        value.textContent = seconds(row.mean);
        bar.appendChild(label);
        bar.appendChild(track);
        bar.appendChild(value);
        wrapper.appendChild(bar);
      });
      el["suite-chart"].appendChild(wrapper);
    });
  }

  function renderSuiteTable(rows) {
    var columns = ["Cities", "Strategy", "Mean", "Median", "Variance", "Fastest",
      "Slowest", "Mean tour", "No tour"];
    var table = el["suite-table"];
    clear(table);

    var head = document.createElement("thead");
    var headRow = document.createElement("tr");
    columns.forEach(function (name) {
      var th = document.createElement("th");
      th.textContent = name;
      headRow.appendChild(th);
    });
    head.appendChild(headRow);
    table.appendChild(head);

    var bestBySize = {};
    rows.forEach(function (row) {
      if (bestBySize[row.size] === undefined || row.mean < bestBySize[row.size]) {
        bestBySize[row.size] = row.mean;
      }
    });

    var body = document.createElement("tbody");
    rows.forEach(function (row) {
      var tr = document.createElement("tr");
      if (row.mean === bestBySize[row.size]) { tr.className = "is-best"; }
      [
        [String(row.size), true],
        [row.label, false],
        [seconds(row.mean), true, "mean"],
        [seconds(row.median), true],
        [row.variance.toFixed(4), true],
        [seconds(row.fastest), true],
        [seconds(row.slowest), true],
        [row.meanTourLength === null ? "--" : Math.round(row.meanTourLength).toLocaleString(), true],
        [String(row.failures), true]
      ].forEach(function (cell) {
        var td = document.createElement("td");
        td.textContent = cell[0];
        if (cell[1]) { td.className = "num" + (cell[2] ? " " + cell[2] : ""); }
        tr.appendChild(td);
      });
      body.appendChild(tr);
    });
    table.appendChild(body);
  }

  // ---------------------------------------------------------------- wiring

  function selectTab(which) {
    var plot = which === "plot";
    el["tab-plot"].setAttribute("aria-selected", String(plot));
    el["tab-suite"].setAttribute("aria-selected", String(!plot));
    el["panel-plot"].hidden = !plot;
    el["panel-suite"].hidden = plot;
  }

  function buildStrategyList() {
    state.config.strategies.forEach(function (strategy, index) {
      var label = document.createElement("label");
      label.className = "strategy";
      var input = document.createElement("input");
      input.type = "radio";
      input.name = "strategy";
      input.value = strategy.key;
      input.checked = strategy.key === "windows";
      var name = document.createElement("span");
      name.className = "strategy__name";
      name.textContent = strategy.label;
      var blurb = document.createElement("span");
      blurb.className = "strategy__blurb";
      blurb.textContent = strategy.blurb;
      label.appendChild(input);
      label.appendChild(name);
      label.appendChild(blurb);
      el.strategies.appendChild(label);
      if (index === state.config.strategies.length - 1 && !el.strategies.querySelector("input:checked")) {
        input.checked = true;
      }
    });
  }

  function wire() {
    el.controls.addEventListener("submit", solve);
    el.cancel.addEventListener("click", cancel);

    el.size.addEventListener("input", updateGuidance);
    el.size.addEventListener("change", function () { updateGuidance(); refreshInstance(); });
    el.seed.addEventListener("change", refreshInstance);
    el["time-limit"].addEventListener("input", updateGuidance);
    el["cross-check"].addEventListener("change", updateGuidance);
    el.strategies.addEventListener("change", updateGuidance);

    el.reroll.addEventListener("click", function () {
      el.seed.value = Math.floor(Math.random() * 9000000);
      refreshInstance();
    });

    document.querySelectorAll('input[name="mode"]').forEach(function (input) {
      input.addEventListener("change", function () { setMode(input.value); });
    });

    el["clear-points"].addEventListener("click", function () {
      state.points = [];
      relabel();
      state.result = null;
      renderReadout(null);
      el.verdict.hidden = true;
      el["tour-path"].textContent = "Place at least three cities.";
      redraw(false);
    });

    el["seed-points"].addEventListener("click", function () {
      api("/api/instance", { mode: "random", size: Number(el.size.value), seed: Number(el.seed.value) })
        .then(function (payload) {
          state.points = payload.points;
          relabel();
          state.result = null;
          renderReadout(null);
          redraw(false);
        }).catch(function (error) { toast(error.message); });
    });

    el.plot.addEventListener("click", onPlotClick);

    ["layer-hulls", "layer-cuts", "layer-check", "layer-labels"].forEach(function (id) {
      el[id].addEventListener("change", function () { redraw(false); });
    });

    el["tab-plot"].addEventListener("click", function () { selectTab("plot"); });
    el["tab-suite"].addEventListener("click", function () { selectTab("suite"); });
    el["suite-form"].addEventListener("submit", runSuite);
    el["suite-cancel"].addEventListener("click", function () {
      if (state.suiteJob) { api("/api/cancel/" + state.suiteJob, {}).catch(function () {}); }
    });
  }

  function boot() {
    api("/api/config").then(function (config) {
      state.config = config;
      el.size.max = Math.min(config.maxCities, 16);
      buildStrategyList();
      buildSuiteControls();
      wire();
      updateGuidance();
      drawGrid();
      // Open on a finished solve so the workbench shows what it does at rest.
      solve();
    }).catch(function (error) {
      toast("Could not reach the workbench server: " + error.message);
    });
  }

  boot();
}());
