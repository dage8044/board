import sys
input=sys.stdin.readline

words = list(map(str, input().rstrip()))
atom = {"H": 1, "C": 12, "O": 16}
stack = []

for i in words:
    if i == "(":
        stack.append(i)
    elif i == ")":
        word = 0
        while True:
            temp = stack.pop()
            if temp == "(":
                break
            word += temp
        stack.append(word)
    elif i in atom:
        stack.append(atom[i])
    else:
        temp = stack.pop()
        stack.append(temp * int(i))

print(sum(stack))