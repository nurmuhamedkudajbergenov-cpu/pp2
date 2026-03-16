n = int(input())

power = 1

while power < n:
    power *= 2

if power == n:
    print("YES")
else:
    print("NO")