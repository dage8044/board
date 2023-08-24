import sys
input=sys.stdin.readline

T = int(input().rstrip())
for i in range(T):
    P, M, F, C = map(int, input().rstrip().split())
    chicken = M // P
    coupon = chicken * C
    # zerochichen은 두영
    zerochicken = chicken + (coupon // F)
    if coupon >= F:
        chicken += (coupon - F) // (F - C) + 1
    print(chicken - zerochicken)