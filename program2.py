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

    #find the peak (guaranteed to be unique) in Θ(n). +1 converts it to its panel number
    peak_index = costs.index(max(costs)) + 1
    opt_cost = float('inf')
    opt_route = []

    #try at most k+1 length-k jumps spanning the peak, including its endpoints
    #each candidate takes O(n/k + 1) time, so all candidates take O(n) since n >= k
    for a in range(max(0, peak_index - k), min(peak_index, n-k) + 1):
        current_route = []
        current_cost = 0
        position = a

        #build the left side backward, noting that earlier panels have no higher costs
        #having jumps of k limit this loop to O(n/k + 1) iterations

        while position > 0:
            current_route.append(position)
            position = max(0, position - k)

        #reverse into forward travel order in O(n/k + 1) time to have increasing panel indexes
        current_route.reverse()
        position = a + k

        #cross to a+k and then jump as far as possible on the non-increasing right side
        #include panel n and its cost
        #this loop takes O(n/k + 1) time
        current_route.append(position)
        while position != n:
            position = min(n, position + k)
            current_route.append(position)

        #sum all landings in O(n/k + 1) time
        #subtract each panel index by 1 since Python indices start at 0
        for panel in current_route:
            current_cost += costs[panel - 1]

        #keep the cheapest round found so far, it will become global optimum after all the candidates have been checked
        #saving the list reference is O(1)
        if current_cost < opt_cost:
            opt_cost = current_cost
            opt_route = current_route

    #overall Θ(n) time: peak scan plus O((k+1)(n/k+1)) = O(n), since k <= n
    #extra space is O(n/k + 1), holding only the current and best routes
    return opt_cost, opt_route



if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program2(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)
