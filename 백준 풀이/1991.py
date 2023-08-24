import sys
input=sys.stdin.readline

N = int(input().rstrip())
arr = []
dp = [[0] * i for i in range(1, N)]

for i in range(N):
    temp = list(map(int, input().rstrip().split()))
    arr.append(temp)
dp.append(temp)
for i in range(N-1, 0, -1):
    for j in range(i):
        dp[i-1][j] = max(dp[i][j] + arr[i-1][j], dp[i][j+1] + arr[i-1][j])
print(dp[0][0])