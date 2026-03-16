from collections import Counter

n = int(input())
nums = []

for i in range(n):
    nums.append(input())

cnt = Counter(nums)

answer = 0
for v in cnt.values():
    if v == 3:
        answer += 1

print(answer)