n = int(input())
nums = list(map(int, input().split()))
count = sum(map(bool, nums))
print(count)