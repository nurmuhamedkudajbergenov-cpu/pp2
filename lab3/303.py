to_digit = {
    "ZER": "0", "ONE": "1", "TWO": "2", "THR": "3", "FOU": "4",
    "FIV": "5", "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9"
}
to_triplet = {v: k for k, v in to_digit.items()}

s = input().strip()

op = ""
for c in s:
    if c in "+-*":
        op = c
        break

left, right = s.split(op)

num1 = ""
for i in range(0, len(left), 3):
    num1 += to_digit[left[i:i+3]]

num2 = ""
for i in range(0, len(right), 3):
    num2 += to_digit[right[i:i+3]]

a = int(num1)
b = int(num2)

if op == "+":
    res = a + b
elif op == "-":
    res = a - b
else:
    res = a * b

res_str = str(res)
ans = ""
for ch in res_str:
    ans += to_triplet[ch]

print(ans)