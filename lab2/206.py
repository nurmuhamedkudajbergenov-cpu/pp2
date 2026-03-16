n = int(input())
nums = input().split()

mx = int(nums[0])
for i in range(1, n):
    if int(nums[i]) > mx:
        mx = int(nums[i])

print(mx)