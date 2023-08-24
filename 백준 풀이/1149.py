import sys
input=sys.stdin.readline

n = int(input())
dp = [[0]*3 for _ in range(n+1)]

for i in range(n):
    temp = (list(map(int, input().rstrip().split())))
    for j in range(3):
        dp[i][j] = temp[j]
        
for i in range(1, n+1):
    dp[i][0] += min(dp[i-1][1], dp[i-1][2]) 
    dp[i][1] += min(dp[i-1][0], dp[i-1][2]) 
    dp[i][2] += min(dp[i-1][0], dp[i-1][1]) 

print(min(dp[-1][0], dp[-1][1], dp[-1][2]))