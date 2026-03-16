n=int(input())
nums = list(map(int, input().split()))
nums = [x * x for x in nums]
print(*nums)