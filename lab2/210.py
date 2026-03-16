n = int(input())
nums = []
while len(nums) < n:
    nums += list(map(int, input().split()))
nums.sort(reverse=True)
print(*nums)