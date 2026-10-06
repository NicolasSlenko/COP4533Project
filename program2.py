from typing import List, Tuple


def program2(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 2
    
    Parameters:
    n (int): number of panels
    k (int): maximum number of positions in a forward jump
    costs (List[int]): the landing costs of the panels

    Returns:
    int:  minimum total energy cost
    List[int]: the indices of the visited panels in increasing order(1-indexed, including n and excluding 0)
    """
    ############################
    # Add your code here
    ############################

    return 0, [1, 2, 3] # replace with your code


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program2(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)