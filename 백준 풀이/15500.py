import sys
input=sys.stdin.readline

N = int(input().rstrip())
a = list(map(int, input().rstrip().split()))
stack1 = []
stack2 = []
big = N
cnt = 0
result = []
for i in a:
    stack1.append(i)
while stack1 or stack2:
    if big in stack1:
        while True:
            temp = stack1.pop()
            if temp == big:
                cnt += 1
                big -= 1
                result.append((1, 3))
                break
            else:
                cnt += 1
                stack2.append(temp)
                result.append((1,2))
    else:
        while True:
            temp = stack2.pop()
            if temp == big:
                cnt += 1
                result.append((2,3))
                big -= 1
                break
            else:
                cnt += 1
                result.append((2,1))
                stack1.append(temp)
print(cnt)
for i in result:
    print(*i)