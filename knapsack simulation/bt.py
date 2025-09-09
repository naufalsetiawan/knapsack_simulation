def knapsack_backtrack(weights, values, capacity, n):
    
    items = list(range(n))
    ratios = [values[i] / weights[i] if weights[i] != 0 else 0 for i in range(n)]

    # sorting
    items.sort(key=lambda i: ratios[i], reverse=True)
    sorted_weights = [weights[i] for i in items]
    sorted_values = [values[i] for i in items]

    best_value = [0]
    best_items = [[]]

    def backtrack(i, cur_weight, cur_value, chosen):
        if i == n:
            if cur_value > best_value[0]:
                best_value[0] = cur_value
                best_items[0] = chosen[:]
            return

        # ambil item
        if cur_weight + sorted_weights[i] <= capacity:
            chosen.append(items[i]) 
            backtrack(i+1, cur_weight + sorted_weights[i], cur_value + sorted_values[i], chosen)
            chosen.pop()

        # skip item 
        backtrack(i+1, cur_weight, cur_value, chosen)

    backtrack(0, 0, 0, [])

    return best_value[0], sorted(best_items[0]) 
