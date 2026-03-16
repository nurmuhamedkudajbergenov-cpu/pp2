n = int(input())
arr = list(map(int, input().split()))
q = int(input())

for _ in range(q):
    parts = input().split()
    op = parts[0]

    if op == "abs":
        for i in range(n):
            if arr[i] < 0:
                arr[i] = -arr[i]

    else:
        x = int(parts[1])

        if op == "add":
            for i in range(n):
                arr[i] += x

        elif op == "multiply":
            for i in range(n):
                arr[i] *= x

        elif op == "power":
            for i in range(n):
                arr[i] = arr[i] ** x

print(*arr)