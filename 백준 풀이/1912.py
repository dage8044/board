import sys
input=sys.stdin.readline

n = int(input().rstrip())
arr = list(map(int, input().rstrip().split()))

for i in range(1, n):
    arr[i] = max(arr[i], arr[i] + arr[i-1])
print(max(arr))