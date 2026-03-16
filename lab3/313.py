nums = list(map(int, input().split()))
primes = []

for x in nums:
    if x < 2:
        continue
    is_prime = True
    i = 2
    while i * i <= x:
        if x % i == 0:
            is_prime = False
            break
        i += 1
    if is_prime:
        primes.append(x)

if len(primes) == 0:
    print("No primes")
else:
    print(*primes)