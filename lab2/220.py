n = int(input())
arr = list(map(int, input().split()))

freq = {}
for x in arr:
    freq[x] = freq.get(x, 0) + 1

max_freq = max(freq.values())
a = None
for x, f in freq.items():
    if f == max_freq:
        if a is None or x < a:
            a = x

print(a)