import sys
n = int(input())
first = True
for i in range(0, n+1, 2):
    if first:
        sys.stdout.write(str(i))
        first = False
    else:
        sys.stdout.write(','+str(i))
sys.stdout.write('\n')