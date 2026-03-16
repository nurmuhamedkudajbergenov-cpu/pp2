n = int(input())
nums = []

while len(nums) < n:
    nums += input().split()

nums = list(map(int, nums))