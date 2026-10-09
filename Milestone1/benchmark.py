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
    n_values = [20000, 40000, 60000, 80000, 100000]
    k = 50
    trials = 20

    # Warm-up run to eliminate cold-start cache/JIT overhead
    dummy = generate_s1(1000)
    program1(1000, k, dummy)
    program2(1000, k, dummy)

    # Benchmark Program 1 (ProblemS1)
    p1_results = []
    for n in n_values:
        total_time = 0.0
        for _ in range(trials):
            costs = generate_s1(n)
            t0 = time.perf_counter()
            program1(n, k, costs)
            t1 = time.perf_counter()
            total_time += (t1 - t0)
        avg_time = total_time / trials
        p1_results.append(avg_time)

    # Benchmark Program 2 (ProblemS2)
    p2_results = []
    for n in n_values:
        total_time = 0.0
        for _ in range(trials):
            costs = generate_s2(n)
            t0 = time.perf_counter()
            program2(n, k, costs)
            t1 = time.perf_counter()
            total_time += (t1 - t0)
        avg_time = total_time / trials
        p2_results.append(avg_time)

    # Print LaTeX filecontents tables
    print("\\begin{filecontents}{p1.dat}")
    print("X   Points   Program1")
    for idx, (n, t) in enumerate(zip(n_values, p1_results), 1):
        print(f"{idx}   {n:<8} {t:.9f}")
    print("\\end{filecontents}\n")

    print("\\begin{filecontents}{p2.dat}")
    print("X   Points   Program2")
    for idx, (n, t) in enumerate(zip(n_values, p2_results), 1):
        print(f"{idx}   {n:<8} {t:.9f}")
    print("\\end{filecontents}")


if __name__ == '__main__':
    run_benchmarks()
