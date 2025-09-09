def knapsack_dp(weights, values, capacity):
    n = len(weights)
    dp = [[0]*(capacity+1) for _ in range(n+1)]
    
    for i in range(1, n+1):
        for w in range(capacity+1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], values[i-1] + dp[i-1][w-weights[i-1]])
            else:
                dp[i][w] = dp[i-1][w]
    
    # item yang dipilih
    res = dp[n][capacity]
    w = capacity
    best_items = []
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == dp[i-1][w]:
            continue
        else:
            best_items.append(i-1)
            res -= values[i-1]
            w -= weights[i-1]
    best_items.reverse()

    return dp[n][capacity], best_items