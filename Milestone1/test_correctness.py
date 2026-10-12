import random
from typing import List
from program1 import program1
from program2 import program2


def dp_reference(n: int, k: int, costs: List[int]) -> int:
    """Return the optimal ProblemG cost with a simple O(nk) DP, used only as a reference."""
    best = [0] + [float('inf')] * n
    for i in range(1, n + 1):
        #cheapest way to land on panel i is its cost plus the cheapest of the k positions before it
        best[i] = costs[i - 1] + min(best[max(0, i - k):i])
    return best[n]


def check_route(n: int, k: int, costs: List[int], cost: int, route: List[int]) -> None:
    """Assert that the route is valid and that its landing costs add up to the reported cost."""
    prev = 0
    for panel in route:
        assert 1 <= panel - prev <= k, f"invalid jump {prev}->{panel} in {route}"
        prev = panel
    assert prev == n, f"route {route} does not end at panel {n}"
    assert sum(costs[panel - 1] for panel in route) == cost, f"reported cost {cost} does not match route {route}"


def generate_s1(n: int, max_cost: int) -> List[int]:
    """Random non-increasing costs for ProblemS1."""
    return sorted((random.randint(1, max_cost) for _ in range(n)), reverse=True)


def generate_s2(n: int, max_cost: int) -> List[int]:
    """Random single-peak costs for ProblemS2, with a peak strictly larger than every other panel."""
    p = random.randint(2, n - 1)
    left = sorted(random.randint(1, max_cost) for _ in range(p - 1))
    right = sorted((random.randint(1, max_cost) for _ in range(n - p)), reverse=True)
    peak = max(left + right) + random.randint(1, 5)
    return left + [peak] + right


def run_tests(trials: int = 100000, max_n: int = 14, max_cost: int = 30) -> None:
    """Compare both programs against an independent DP reference on valid random inputs."""
    random.seed(4533)
    #examples from the assignment
    assert program1(8, 3, [20, 18, 16, 14, 12, 10, 8, 6]) == (32, [3, 6, 8])
    assert program2(10, 4, [1, 2, 4, 9, 12, 10, 6, 4, 3, 1]) == (11, [3, 7, 10])

    for _ in range(trials):
        n = random.randint(1, max_n)
        k = random.randint(1, n)

        costs = generate_s1(n, max_cost)
        cost, route = program1(n, k, costs)
        check_route(n, k, costs, cost, route)
        assert cost == dp_reference(n, k, costs), f"Program 1 not optimal: n={n} k={k} costs={costs}"

        #ProblemS2 needs a peak strictly inside the row, so n >= 3
        n = random.randint(3, max_n)
        k = random.randint(1, n)
        costs = generate_s2(n, max_cost)
        cost, route = program2(n, k, costs)
        check_route(n, k, costs, cost, route)
        assert cost == dp_reference(n, k, costs), f"Program 2 not optimal: n={n} k={k} costs={costs}"

    print(f"All {trials} random trials per program passed.")


if __name__ == '__main__':
    run_tests()
