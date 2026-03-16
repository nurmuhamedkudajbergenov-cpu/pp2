n = int(input())
nums = list(map(int, input().split()))
square = sum(map(lambda x: x **2 , nums))
print(square)
