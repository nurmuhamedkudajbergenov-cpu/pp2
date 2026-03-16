def countdown(n):
    for i in range(n, -1, -1):
        yield i

n = int(input())
for v in countdown(n):
    print(v)