import sys
input=sys.stdin.readline

k = int(input().rstrip())
a = [0 for i in range(k+1)]
a[0] = 1
a[1] = 0
 
b = [0 for i in range(k+1)]
b[0] = 0
b[1] = 1
 
for i in range(2, k+1):
    a[i] = a[i - 1] + a[i - 2]
    b[i] = b[i - 1] + b[i - 2]
print(a[k], b[k])