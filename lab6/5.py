s = input()
vowels = "aeiou"
vov = any(c in vowels for c in s)
if vov:
    print("Yes")
else:
    print("No")