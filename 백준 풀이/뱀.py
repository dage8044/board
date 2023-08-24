import sys
input = sys.stdin.readline
from collections import deque

n = int(input().rstrip())
k = int(input().rstrip())

gameboard = [[0] * (n+1) for _ in range(n+1)]
for i in range(k):
    x, y = map(int, input().rstrip().split())
    gameboard[x][y] = 2

l = int(input().rstrip())
dic = []
for i in range(l):
    dic.append(input().rstrip().split())

dx = [0, 1, 0, -1]  
dy = [1, 0, -1, 0]  
x, y, d = 1, 1, 0
snake = deque([(1,1)])
time = 0
cnt = 0

while True:
    nx, ny = x+dx[d], y+dy[d]
    time += 1
    
    if nx <= 0 or ny <= 0 or nx > n or ny > n or (nx, ny) in snake:
        break

    snake.appendleft((nx, ny))
    x, y = nx, ny
    if gameboard[x][y] != 2:
        i, j = snake.pop()
        gameboard[i][j] = 0

    gameboard[x][y] = 1

    if cnt < l:
        if time == int(dic[cnt][0]):
            if dic[cnt][1] == 'D':
                d = (d + 1) % 4
                cnt += 1
            else:
                d = (d - 1) % 4
                cnt += 1
print(time)
