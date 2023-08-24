def is_connectable(a, b, is_swapped):
    max_step = min(len(a), len(b))
    for cnt in range(1, max_step + 1):
        same = True
        for i in range(cnt):
            if a[len(a) - cnt + i] != b[i]:
                same = False
                break
        if same:
            return True
    
    if is_swapped:
        return False
    else:
        return is_connectable(b, a, True)

n = int(input())
arr = []
for _ in range(n):
    arr.append(input())

count = 0
for i in range(n):
    for j in range(i + 1, n):
        count += is_connectable(arr[i], arr[j], False)

print(count)