import sys
input=sys.stdin.readline
import heapq

t = int(input().rstrip())

for i in range(t):
    k = int(input().rstrip())
    minheap, maxheap = [], []
    visited = [False] * k

    for j in range(k):
        com, num = input().split()

        if com == 'I':
            heapq.heappush(minheap, (int(num), j))
            heapq.heappush(maxheap, (-int(num), j))
            visited[j] = True

        else:
            if num == '1':
                while maxheap and not visited[maxheap[0][1]]:
                    heapq.heappop(maxheap)
                if maxheap:
                    visited[maxheap[0][1]] = False
                    heapq.heappop(maxheap)
            else:
                while minheap and not visited[minheap[0][1]]:
                    heapq.heappop(minheap)
                if minheap:
                    visited[minheap[0][1]] = False
                    heapq.heappop(minheap)

    while minheap and not visited[minheap[0][1]]:
        heapq.heappop(minheap)
    while maxheap and not visited[maxheap[0][1]]:
        heapq.heappop(maxheap)

    if not minheap or not maxheap:
        print("EMPTY")
    else:
        print(-maxheap[0][0], minheap[0][0])