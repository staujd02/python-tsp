"""Computation layer between the research code and the Hull Cut Workbench UI.

Everything here is pure: give it parameters, get back plain dictionaries that
survive a JSON round trip. The web layer never touches the solver directly.
"""

from copy import deepcopy
from itertools import permutations
from random import seed as set_seed
from time import perf_counter

from source.utilities.exclusion_generator import ExclusionGenerator
from source.utilities.graham_scan import GrahamScan
from source.utilities.matrix_builder import MatrixBuilder
from source.utilities.solver import Solver
from source.utilities.transformer import Transformer

# GraphStringMuxer indexes the graph with ord(label) - 65 and reads the
# destination out of a fixed string offset, so every label has to be a single
# letter. That caps an instance at the alphabet.
MAX_CITIES = 26
MIN_CITIES = 3

# Above this the exact cross-check would outrun the solver it is checking.
BRUTE_FORCE_LIMIT = 9


def _no_exclusions(_points):
    return {}


def _hull_only(points):
    return ExclusionGenerator.generateExclusionDictionary(GrahamScan.getConvexHull(points))


STRATEGIES = [
    {
        "key": "none",
        "label": "No elimination",
        "blurb": "Every edge stays in the augment list. The baseline.",
        "fn": _no_exclusions,
    },
    {
        "key": "hull",
        "label": "Outer hull",
        "blurb": "Cuts chords of the outermost convex hull only.",
        "fn": _hull_only,
    },
    {
        "key": "rings",
        "label": "Hull rings",
        "blurb": "Peels the set into nested hulls, cutting each ring's chords.",
        "fn": ExclusionGenerator.generateExclusionsByHullRings,
    },
    {
        "key": "deep",
        "label": "Deep cut",
        "blurb": "Adds cuts from each outer point across the hulls beneath it.",
        "fn": ExclusionGenerator.generateExclusionsWithDeepCutsAroundHullRings,
    },
    {
        "key": "web",
        "label": "Deep web",
        "blurb": "Re-hulls every outer point against each interior ring.",
        "fn": ExclusionGenerator.generateExclusionDictionaryDeepWebCut,
    },
    {
        "key": "windows",
        "label": "Deep web + windows",
        "blurb": "Deep web with the windowed neighbour pass.",
        "fn": ExclusionGenerator.generateExclusionDictionaryDeepWebCutWithWindows,
    },
]

STRATEGY_BY_KEY = {s["key"]: s for s in STRATEGIES}


def strategy_catalogue():
    """The strategy list, minus the function objects, for the UI."""
    return [{k: v for k, v in s.items() if k != "fn"} for s in STRATEGIES]


class InstanceError(ValueError):
    pass


def build_random_instance(size, seed_value):
    size = int(size)
    if not MIN_CITIES <= size <= MAX_CITIES:
        raise InstanceError(
            "Pick between %d and %d cities. Labels are single letters, so %d is the ceiling."
            % (MIN_CITIES, MAX_CITIES, MAX_CITIES)
        )
    set_seed(int(seed_value))
    matrix = []
    points = MatrixBuilder.populateEuclideanMatrix(matrix, size)
    return points, matrix


def build_instance_from_points(coords):
    if not MIN_CITIES <= len(coords) <= MAX_CITIES:
        raise InstanceError("Place between %d and %d cities." % (MIN_CITIES, MAX_CITIES))
    labels = MatrixBuilder.getUniqueLabels(len(coords))
    points = [[int(round(c[0])), int(round(c[1])), labels[i]] for i, c in enumerate(coords)]
    matrix = []
    MatrixBuilder.populateEuclideanMatrixFromPoints(matrix, points)
    return points, matrix


def hull_rings(points):
    """The nested convex hulls, as label lists, for the plot underlay."""
    _, rings = ExclusionGenerator.createHullRings(deepcopy(points), 2)
    return [[p[2] for p in ring] for ring in rings]


def exclusion_pairs(exclusions):
    """Flatten the exclusion dictionary into unique unordered label pairs."""
    seen = set()
    pairs = []
    for origin, destinations in exclusions.items():
        for destination in destinations:
            key = tuple(sorted((origin, destination)))
            if key in seen:
                continue
            seen.add(key)
            pairs.append(list(key))
    return pairs


def _distance_table(points):
    table = {}
    for a in points:
        for b in points:
            if a[2] == b[2]:
                continue
            table[(a[2], b[2])] = MatrixBuilder.calculateDistance(a[0], a[1], b[0], b[1])
    return table


def _tour_length(tour, table):
    return sum(table[(tour[i], tour[i + 1])] for i in range(len(tour) - 1))


def _parse_tour(graph):
    """Graph.getVectorPath renders the tour as (A->D->C->A)."""
    return graph.getVectorPath().strip("()").split("->")


def solve(points, matrix, strategy_key, cross_check=True):
    """Run one instance through the pipeline and describe what happened."""
    strategy = STRATEGY_BY_KEY.get(strategy_key)
    if strategy is None:
        raise InstanceError("Unknown elimination strategy: %r" % (strategy_key,))

    size = len(points)
    headers = MatrixBuilder.getUniqueLabels(size)

    cut_start = perf_counter()
    exclusions = strategy["fn"](deepcopy(points))
    cut_seconds = perf_counter() - cut_start

    zero_graph, vectors = Transformer(matrix, headers, exclusions).fetchSolvePieces()

    solve_start = perf_counter()
    graph = Solver().solve(zero_graph, vectors)
    solve_seconds = perf_counter() - solve_start

    table = _distance_table(points)
    total_edges = size * (size - 1)
    # One zero vector per column is held out of the augment list; the rest of
    # the shortfall is what the cuts removed.
    surviving_edges = len(vectors) + size

    result = {
        "strategy": strategy_key,
        "size": size,
        "solveSeconds": solve_seconds,
        "cutSeconds": cut_seconds,
        "augmentVectors": len(vectors),
        "totalEdges": total_edges,
        "survivingEdges": surviving_edges,
        "eliminatedEdges": total_edges - surviving_edges,
        "exclusionPairs": exclusion_pairs(exclusions),
        "hullRings": hull_rings(points),
        "solved": graph is not None,
    }

    if graph is None:
        result["tour"] = None
        result["tourLength"] = None
        result["reducedCost"] = None
        result["note"] = (
            "The augment list ran out before a valid tour appeared. The cuts "
            "removed an edge the optimal tour needed."
        )
    else:
        tour = _parse_tour(graph)
        result["tour"] = tour
        result["tourLength"] = _tour_length(tour, table)
        result["reducedCost"] = graph.getWeight()

    if cross_check:
        result["crossCheck"] = _cross_check(points, table, result.get("tourLength"))
    return result


def _cross_check(points, table, claimed_length):
    """Independently look for the optimum so a wrong tour cannot go unnoticed."""
    labels = [p[2] for p in points]
    started = perf_counter()
    if len(labels) <= BRUTE_FORCE_LIMIT:
        best, length = _brute_force(labels, table)
        method = "exact"
        headline = "Exhaustive search over every tour."
    else:
        best, length = _two_opt(labels, table)
        method = "heuristic"
        headline = "Nearest neighbour refined by 2-opt. A bound, not a proof."

    check = {
        "method": method,
        "headline": headline,
        "tour": best,
        "tourLength": length,
        "seconds": perf_counter() - started,
    }
    if claimed_length is None:
        check["verdict"] = "unknown"
    elif claimed_length == length:
        check["verdict"] = "match"
    elif claimed_length < length:
        check["verdict"] = "better"
    else:
        check["verdict"] = "worse"
    check["gap"] = None if claimed_length is None else claimed_length - length
    return check


def _brute_force(labels, table):
    start = labels[0]
    rest = labels[1:]
    best = None
    best_length = None
    for order in permutations(rest):
        tour = [start] + list(order) + [start]
        length = _tour_length(tour, table)
        if best_length is None or length < best_length:
            best_length = length
            best = tour
    return best, best_length


def _two_opt(labels, table):
    start = labels[0]
    unvisited = set(labels[1:])
    tour = [start]
    while unvisited:
        here = tour[-1]
        nearest = min(unvisited, key=lambda other: table[(here, other)])
        unvisited.remove(nearest)
        tour.append(nearest)
    tour.append(start)

    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour) - 1):
                a, b, c, d = tour[i - 1], tour[i], tour[j], tour[j + 1]
                if a == c or b == d:
                    continue
                delta = (table[(a, c)] + table[(b, d)]) - (table[(a, b)] + table[(c, d)])
                if delta < 0:
                    tour[i:j + 1] = list(reversed(tour[i:j + 1]))
                    improved = True
    return tour, _tour_length(tour, table)
