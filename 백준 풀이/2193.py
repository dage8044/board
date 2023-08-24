import sys
input=sys.stdin.readline

n = int(input().rstrip())
dp = [1 for _ in range(n)]

for i in range(2, n):
    dp[i] = dp[i-1] + dp[i-2]
print(dp[-1])
