import sys
input=sys.stdin.readline

n, m = map(int, input().rstrip().split())
arr = []
for i in range(n):
    arr.append(int(input().rstrip()))

left = 0
right = max(arr) * m
result = max(arr) * m

while (left <= right):
    people = 0   
    mid = (left + right) // 2 
    for i in range(n):
        people += mid // arr[i]
    if (people >= m):
        right = mid - 1
        result = min(result, mid)
    else:
        left = mid + 1

print(result)