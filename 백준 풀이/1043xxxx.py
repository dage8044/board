import sys
input = sys.stdin.readline

n, m = map(int, input().rstrip().split())
truth = set(input().rstrip().split()[1:])
party = []

for i in range(m):
    party.append(set(input().rstrip().split()[1:]))

for people in party:
    if people in truth:
        for person in people:
            truth.add(person)

cnt = 0
for people in party:
    if people & truth:
        continue
    cnt += 1

print(cnt)