"""Runs one job in its own process and reports back as JSON lines on stdout.

The solver is a tight priority-queue loop with no cancellation hook, and search
time grows steeply with the city count. Isolating a run in a child process is
what makes Cancel and Time limit real: the parent kills the process.

Protocol: the job description arrives as one JSON object on stdin. Each line
written to stdout is one event -- progress, result, or error.
"""

import json
import statistics
import sys
import traceback

from source.webapp import tsp_service


def emit(event, **payload):
    payload["event"] = event
    sys.stdout.write(json.dumps(payload) + "\n")
    sys.stdout.flush()


def _instance(job):
    if job.get("mode") == "custom":
        return tsp_service.build_instance_from_points(job["coords"])
    return tsp_service.build_random_instance(job["size"], job["seed"])


def run_solve(job):
    points, matrix = _instance(job)
    emit("instance", points=points)
    result = tsp_service.solve(
        points,
        matrix,
        job["strategy"],
        cross_check=job.get("crossCheck", True),
    )
    result["points"] = points
    result["seed"] = job.get("seed")
    emit("result", data=result)


def run_suite(job):
    """Every selected strategy against the same instances, size by size."""
    sizes = job["sizes"]
    trials = int(job["trials"])
    strategies = job["strategies"]
    total = len(sizes) * trials * len(strategies)
    done = 0
    rows = []

    for size in sizes:
        instances = []
        for trial in range(trials):
            seed_value = int(job["seed"]) + trial
            instances.append(tsp_service.build_random_instance(size, seed_value))

        for strategy_key in strategies:
            label = tsp_service.STRATEGY_BY_KEY[strategy_key]["label"]
            seconds = []
            lengths = []
            failures = 0
            for points, matrix in instances:
                emit(
                    "progress",
                    done=done,
                    total=total,
                    message="%d cities / %s / trial %d of %d"
                    % (size, label, len(seconds) + 1, trials),
                )
                run = tsp_service.solve(points, matrix, strategy_key, cross_check=False)
                seconds.append(run["solveSeconds"] + run["cutSeconds"])
                if run["solved"]:
                    lengths.append(run["tourLength"])
                else:
                    failures += 1
                done += 1

            mean = statistics.mean(seconds)
            rows.append(
                {
                    "size": size,
                    "strategy": strategy_key,
                    "label": label,
                    "trials": trials,
                    "mean": mean,
                    "median": statistics.median(seconds),
                    "variance": statistics.pvariance(seconds, mean),
                    "fastest": min(seconds),
                    "slowest": max(seconds),
                    "meanTourLength": statistics.mean(lengths) if lengths else None,
                    "failures": failures,
                }
            )

    emit("progress", done=total, total=total, message="Complete")
    emit("result", data={"rows": rows, "sizes": sizes, "trials": trials})


def main():
    try:
        job = json.loads(sys.stdin.read())
    except ValueError as error:
        emit("error", message="Could not read the job description: %s" % error)
        return 1

    try:
        if job.get("kind") == "suite":
            run_suite(job)
        else:
            run_solve(job)
    except tsp_service.InstanceError as error:
        emit("error", message=str(error))
        return 1
    except MemoryError:
        emit(
            "error",
            message="The search ran out of memory. The queue grows fast past a "
            "dozen cities -- try a smaller instance or a deeper cut.",
        )
        return 1
    except Exception:
        emit("error", message="The solver stopped unexpectedly.", detail=traceback.format_exc())
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
