import csv
import json
import platform
import random
import statistics
import time
from pathlib import Path
from typing import List

from program1 import program1
from program2 import program2


def generate_s1(n: int) -> List[int]:
    """Generate valid non-increasing costs, all below 100000."""
    return sorted((random.randint(1, 99999) for _ in range(n)), reverse=True)


def generate_s2(n: int) -> List[int]:
    """Reserve a unique interior peak and keep both sides strictly below it."""
    p = random.randint(2, n - 1)
    peak = random.randint(2, 99999)
    left = sorted(random.randint(1, peak - 1) for _ in range(p - 1))
    right = sorted((random.randint(1, peak - 1) for _ in range(n - p)), reverse=True)
    return left + [peak] + right


def validate_input(n, k, costs, problem):
    """Check constraints before timing, so invalid data cannot enter the plots."""
    assert 1 <= k <= n < 100000 and len(costs) == n
    assert all(1 <= cost < 100000 for cost in costs)
    if problem == 1:
        assert all(costs[i] >= costs[i + 1] for i in range(n - 1))
    else:
        p = costs.index(max(costs))
        assert 0 < p < n - 1 and costs.count(costs[p]) == 1
        assert all(costs[i] <= costs[i + 1] for i in range(p))
        assert all(costs[i] >= costs[i + 1] for i in range(p, n - 1))


def save_input(directory, problem, n, k, costs):
    """Keep one example stdin file for each measured configuration."""
    path = directory / f"program{problem}_n{n}_k{k}.txt"
    path.write_text(f"{n} {k}\n" + " ".join(map(str, costs)) + "\n", encoding="utf-8")


def measure(function, n, k, costs, repeats):
    # Warm up this input, then time a batch to reduce timer overhead per call.
    function(n, k, costs)
    start = time.perf_counter()
    for _ in range(repeats):
        function(n, k, costs)
    return (time.perf_counter() - start) / repeats


def summarize(n, k, times):
    return {"n": n, "k": k, "mean": statistics.mean(times),
            "std": statistics.stdev(times)}


def run_benchmarks():
    """Save measured samples, input examples, and the report's plot tables."""
    seed, trials = 4533, 20
    random.seed(seed)
    n_values = [20000, 40000, 60000, 80000, 99999]
    k_values = [10, 25, 50, 100, 200]
    k, n_fixed = 50, 50000
    repeats = {1: 50, 2: 5}
    directory = Path(__file__).resolve().parent / "experiments"
    inputs = directory / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    raw = []
    results = {"seed": seed, "trials": trials, "repeats": repeats,
               "python": platform.python_version(), "system": platform.platform(),
               "processor": platform.processor(), "vary_n": {}, "vary_k": {}}

    for problem, function, generator in [(1, program1, generate_s1), (2, program2, generate_s2)]:
        rows = []
        for n in n_values:
            times = []
            for trial in range(trials):
                costs = generator(n)
                validate_input(n, k, costs, problem)
                if trial == 0:
                    save_input(inputs, problem, n, k, costs)
                seconds = measure(function, n, k, costs, repeats[problem])
                times.append(seconds)
                raw.append(["vary_n", problem, n, k, trial + 1, seconds])
            rows.append(summarize(n, k, times))

        # Fit time = c * work by least squares with zero intercept.
        work = [row["n"] / k if problem == 1 else row["n"] for row in rows]
        fit = sum(x * row["mean"] for x, row in zip(work, rows)) / sum(x * x for x in work)
        for x, row in zip(work, rows):
            row["fitted"] = fit * x
        results["vary_n"][str(problem)] = {"fit": fit, "rows": rows}

    times_by_k = {problem: {cur_k: [] for cur_k in k_values} for problem in [1, 2]}
    for trial in range(trials):
        # Reuse each trial's costs across k, so changes in k are compared on the same data.
        for problem, function, generator in [(1, program1, generate_s1), (2, program2, generate_s2)]:
            costs = generator(n_fixed)
            for cur_k in k_values:
                validate_input(n_fixed, cur_k, costs, problem)
                if trial == 0:
                    save_input(inputs, problem, n_fixed, cur_k, costs)
                seconds = measure(function, n_fixed, cur_k, costs, repeats[problem])
                times_by_k[problem][cur_k].append(seconds)
                raw.append(["vary_k", problem, n_fixed, cur_k, trial + 1, seconds])
    for problem in [1, 2]:
        results["vary_k"][str(problem)] = [
            summarize(n_fixed, cur_k, times_by_k[problem][cur_k]) for cur_k in k_values]

    with (directory / "timings.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["study", "program", "n", "k", "trial", "seconds_per_call"])
        writer.writerows(raw)
    (directory / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    for problem in [1, 2]:
        print(f"\\begin{{filecontents*}}[overwrite]{{p{problem}.dat}}")
        print("Points Mean Std Theoretical")
        for row in results["vary_n"][str(problem)]["rows"]:
            print(f"{row['n']} {row['mean']:.12f} {row['std']:.12f} {row['fitted']:.12f}")
        print("\\end{filecontents*}\n")
    print("\\begin{filecontents*}[overwrite]{varying_k.dat}")
    print("K Program1 Std1 Program2 Std2")
    for row1, row2 in zip(results["vary_k"]["1"], results["vary_k"]["2"]):
        print(f"{row1['k']} {row1['mean']:.12f} {row1['std']:.12f} {row2['mean']:.12f} {row2['std']:.12f}")
    print("\\end{filecontents*}")


if __name__ == '__main__':
    run_benchmarks()
