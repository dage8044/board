import sys
input = sys.stdin.readline

n = int(input().rstrip())
stack = list(map(int, input().rstrip().split()))
temp = []
target = 1

while stack or temp:
    if stack:
        if stack[0] == target:   
            stack.pop(0)   
            target += 1
        else:
            if temp:
                if temp[-1] == target:
                    temp.pop()
                    target += 1
                else:
                    temp.append(stack.pop(0))
            else:
                temp.append(stack.pop(0))
    else:
        if temp[-1] == target:
            temp.pop()
            target += 1
        else:
            break
if stack or temp:
    print("Sad")
else:
    print("Nice")

    