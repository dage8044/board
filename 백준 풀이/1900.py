import sys
input=sys.stdin.readline
N=int(input())
lis=[]
for i in range(1,N+1):
    a,b=map(int,input().split())
    lis.append([(b-1)/a,i])
print(lis)
lis.sort()
print(lis)
for i in range(N):
    print(lis[N-i-1][1])