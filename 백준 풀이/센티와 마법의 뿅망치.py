import sys
input=sys.stdin.readline
import heapq

n, h, t = map(int, input().rstrip().split())
cnt = 0

giants = []
for _ in range(n):
    heapq.heappush(giants, -int(input().rstrip())) 


for i in range(t):
    a = heapq.heappop(giants)
    if abs(a) < h:
        heapq.heappush(giants, a) 
        break
    elif abs(a) == 1:
        heapq.heappush(giants, a)
    else:
        a = -(abs(a) // 2)
        heapq.heappush(giants, a) 
        cnt+=1


if abs(min(giants)) < h:
    print('YES')
    print(cnt)
else:
    print('NO')
    print(abs(heapq.heappop(giants)))