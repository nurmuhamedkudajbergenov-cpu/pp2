n = int(input())
a, b = 0, 1
res = []
for _ in range(n):
    res.append(a)
    a, b = b, a+b
print(','.join(map(str, res)))