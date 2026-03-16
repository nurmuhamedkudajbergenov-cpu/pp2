n=int(input())
for i in range(10):
    for j in range(10):
        if i*j==n:
            print("Yes")
            break
print("No")       