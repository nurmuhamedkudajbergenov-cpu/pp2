n = int(input())
nums = list(map(int, input().split()))
low=int(min(nums))
up=int(max(nums))
li=nums.index(low)
while up in nums:
    ui=nums.index(up)
    nums[ui]=nums[li]
print(*nums)
