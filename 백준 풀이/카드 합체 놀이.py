import sys
input=sys.stdin.readline
import heapq

n, m = map(int, input().rstrip().split())
card = []
arr = list(map(int, input().rstrip().split()))
result = 0

for i in arr:
    heapq.heappush(card, i)

for i in range(m):
    temp1 = heapq.heappop(card)
    temp2 = heapq.heappop(card)
    heapq.heappush(card, temp1+temp2)
    heapq.heappush(card, temp1+temp2)

result = sum(card)
print(result)