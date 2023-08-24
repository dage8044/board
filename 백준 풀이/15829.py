import sys
input=sys.stdin.readline

l = int(input().rstrip())
words = input().rstrip()
result = 0
cnt = 0
for i in words:
    result += (ord(i) - 96) * (31**cnt)
    cnt += 1
print(result % 1234567891)