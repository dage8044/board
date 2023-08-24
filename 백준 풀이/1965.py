import sys
input=sys.stdin.readline

n = int(input().rstrip())
dp = [1] * n
box = list(map(int, input().rstrip().split()))

for i in range(n):
    for j in range(i):
        if box[i] > box[j]:
            dp[i] = max(dp[i],dp[j]+1)
print(max(dp))