a = list(map(int, input().split()))
b = list(map(int, input().split()))
skalyar = 0
for x, y in zip(a , b):
    skalyar += x * y 
print(skalyar)
