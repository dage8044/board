import sys
input=sys.stdin.readline

def bfs(x,y):
    result = 1
    queue = set([(x,y,arr[x][y])])  
    while queue:
        x,y,visited = queue.pop()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx >= 0 and ny >= 0 and nx < R and ny < C and arr[nx][ny] not in visited:  
                queue.add((nx,ny,visited + arr[nx][ny]))
                result = max(result,len(visited)+1)
    return result

R,C = map(int, input().rstrip().split())
arr=[list(input().rstrip()) for i in range(R)] 
dx=[1,-1,0,0] 
dy=[0,0,1,-1]
             
print(bfs(0,0))