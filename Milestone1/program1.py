from typing import List, Tuple


def program1(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 1
    
    Parameters:
    n (int): number of panels
    k (int): maximum number of positions in a forward jump
    costs (List[int]): the landing costs of the panels

    Returns:
    int:  minimum total energy cost
    List[int]: the indices of the visited panels in increasing order(1-indexed, including n and excluding 0)
    """
   
    total_cost = 0
    #Position 0 is the free starting dock, will remove it from the returned route
    visited_panels = [0]

    #In S1, costs never increase when going right, so the farthest reachable
    #panel is among the cheapest reachable panels, even when costs tie

    #The loop runs ⌈n/k⌉ times total, so its time is Θ(⌈n/k⌉). List appends take amortized constant time.
    while visited_panels[-1] < n:

        #ensure robot always ends on the last panel, as required
        next_panel = min(n, visited_panels[-1] + k)
        #subtract 1 to convert the panel number to its Python list index (1 based)
        total_cost += costs[next_panel - 1]

        #reuse visited_panels to keep track of last visited panel p
        visited_panels.append(next_panel)

                        
    return total_cost, visited_panels[1:] #slice copies visited route, also Θ(⌈n/k⌉)


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program1(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)
