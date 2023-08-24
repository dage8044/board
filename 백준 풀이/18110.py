import sys
input=sys.stdin.readline

def round(num):  
    if num - int(num) >= 0.5:
        num = int(num) + 1
    else:
        num = int(num)
    return num

n = int(input().rstrip())
q = []

for _ in range(n):
    q.append(int(input().rstrip()))

q.sort()
if n:
    num = round(n * 0.15)
    if num > 0: 
        q = q[num : -num]
    print(round(sum(q) / (n - num*2)))
else:
    print(0)