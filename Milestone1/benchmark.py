import time
import random
from typing import List
from program1 import program1
from program2 import program2


def generate_s1(n: int) -> List[int]:
    """Generate monotonically non-increasing costs for ProblemS1."""
    costs = [random.randint(1, 100000) for _ in range(n)]
    costs.sort(reverse=True)
    return costs


def generate_s2(n: int) -> List[int]:
    """Generate unimodal single-peak costs for ProblemS2."""
    p = random.randint(2, n - 1)
    left = sorted([random.randint(1, 100000) for _ in range(p - 1)])
    peak = (left[-1] if left else 1000) + random.randint(100, 5000)
    right = sorted([random.randint(1, 100000) for _ in range(n - p)], reverse=True)
    return left + [peak] + right


def run_benchmarks():
    """Run performance benchmarks over multiple trials and output pgfplots data."""
    import math

    n_values = [20000, 40000, 60000, 80000, 100000]
    k = 50
    trials = 20

    # Warm-up run to eliminate cold-start cache/JIT overhead
    program1(1000, k, generate_s1(1000))
    program2(1000, k, generate_s2(1000))

    # Benchmark Program 1 (ProblemS1) across n
    p1_means = []
    p1_stds = []
    for n in n_values:
        times = []
        for _ in range(trials):
            costs = generate_s1(n)
            t0 = time.perf_counter()
            program1(n, k, costs)
            t1 = time.perf_counter()
            times.append(t1 - t0)
        mean_t = sum(times) / trials
        var_t = sum((x - mean_t) ** 2 for x in times) / (trials - 1)
        std_t = math.sqrt(var_t)
        p1_means.append(mean_t)
        p1_stds.append(std_t)

    # Benchmark Program 2 (ProblemS2) across n
    p2_means = []
    p2_stds = []
    for n in n_values:
        times = []
        for _ in range(trials):
            costs = generate_s2(n)
            t0 = time.perf_counter()
            program2(n, k, costs)
            t1 = time.perf_counter()
            times.append(t1 - t0)
        mean_t = sum(times) / trials
        var_t = sum((x - mean_t) ** 2 for x in times) / (trials - 1)
        std_t = math.sqrt(var_t)
        p2_means.append(mean_t)
        p2_stds.append(std_t)

    # Multi-variable experiment: Varying k at fixed n = 50,000
    k_values = [10, 25, 50, 100, 200]
    n_fixed = 50000
    p1_k_means = []
    p2_k_means = []
    for cur_k in k_values:
        times1 = []
        times2 = []
        for _ in range(trials):
            c1 = generate_s1(n_fixed)
            t0 = time.perf_counter()
            program1(n_fixed, cur_k, c1)
            t1 = time.perf_counter()
            times1.append(t1 - t0)

            c2 = generate_s2(n_fixed)
            t0 = time.perf_counter()
            program2(n_fixed, cur_k, c2)
            t1 = time.perf_counter()
            times2.append(t1 - t0)
        p1_k_means.append(sum(times1) / trials)
        p2_k_means.append(sum(times2) / trials)

    # Fitted asymptotic constant c1: mean_t = c1 * (n / k)
    c1_fit = sum(m / (n / k) for n, m in zip(n_values, p1_means)) / len(n_values)
    # Fitted asymptotic constant c2: mean_t = c2 * n
    c2_fit = sum(m / n for n, m in zip(n_values, p2_means)) / len(n_values)

    # Print LaTeX filecontents tables
    print("% Table 1: Program 1 with Error Bars & Theoretical Fit")
    print("\\begin{filecontents*}[overwrite]{p1.dat}")
    print("X   Points   Mean          Std           Theoretical")
    for idx, (n, m, s) in enumerate(zip(n_values, p1_means, p1_stds), 1):
        theo = c1_fit * (n / k)
        print(f"{idx}   {n:<8} {m:.9f} {s:.9f} {theo:.9f}")
    print("\\end{filecontents*}\n")

    print("% Table 2: Program 2 with Error Bars & Theoretical Fit")
    print("\\begin{filecontents*}[overwrite]{p2.dat}")
    print("X   Points   Mean          Std           Theoretical")
    for idx, (n, m, s) in enumerate(zip(n_values, p2_means, p2_stds), 1):
        theo = c2_fit * n
        print(f"{idx}   {n:<8} {m:.9f} {s:.9f} {theo:.9f}")
    print("\\end{filecontents*}\n")

    print("% Table 3: Multi-variable Exploration (Varying k at n = 50,000)")
    print("\\begin{filecontents*}[overwrite]{varying_k.dat}")
    print("X   K        Program1      Program2")
    for idx, (kv, t1, t2) in enumerate(zip(k_values, p1_k_means, p2_k_means), 1):
        print(f"{idx}   {kv:<8} {t1:.9f} {t2:.9f}")
    print("\\end{filecontents*}")


if __name__ == '__main__':
    run_benchmarks()
