import sys
input=sys.stdin.readline

K, N = map(int, input().split())
line = []
for i in range(K):
    line.append(int(input().rstrip()))
start, end = 1, max(line) 

while start <= end: 
    mid = (start + end) // 2 
    cnt = 0 
    for i in line:
        cnt += i // mid      
    if cnt >= N: 
        start = mid + 1
    else:
        end = mid - 1
print(end)