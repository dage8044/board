import sys
input=sys.stdin.readline
from collections import Counter
n = int(input().rstrip())
a = input().rstrip()
b = input().rstrip()
vowel = ['a', 'e', 'i', 'o', 'u']
first = True
second = True
third = True

temp1 = []
temp2 = []

if a[0] != b[0] or a[-1] != b[-1]:
    first = False
for i in range(n):
    if a[i] not in vowel:
        temp1.append(a[i])
    if b[i] not in vowel:
        temp2.append(b[i])
if temp1 != temp2:
    second = False
if Counter(a) != Counter(b):
    third = False
    
if first and second and third:
    print('YES')
else:
    print('NO')