n,l,r = map(int, input().split())
nums = list(map(int, input().split()))
nums[l-1:r] = reversed(nums[l-1:r])
print(*nums)