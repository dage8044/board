import sys
input=sys.stdin.readline
import heapq

n = int(input().rstrip())
cards = []
cnt = 0
for i in range(n):
    cards.append(int(input().rstrip()))
heapq.heapify(cards)
if n == 1:
    print(0)
else:
    while len(cards) > 1:
        temp1 = heapq.heappop(cards)
        temp2 = heapq.heappop(cards)
        cnt += temp1 + temp2
        heapq.heappush(cards, temp1+temp2)
    print(cnt)