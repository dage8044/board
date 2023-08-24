import sys
input=sys.stdin.readline

t = int(input().rstrip())

for i in range(t):
    n = int(input().rstrip())
    dp = [1 for _ in range(n+1)]
    for j in range(3, n):
        dp[j] = dp[j-2] + dp[j-3]
    print(dp[n-1])