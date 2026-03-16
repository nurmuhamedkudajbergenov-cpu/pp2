n = input().strip()

valid = True
for ch in n:
    digit = int(ch)
    if digit % 2 != 0:
        valid = False
        break

if valid:
    print("Valid")
else:
    print("Not valid")