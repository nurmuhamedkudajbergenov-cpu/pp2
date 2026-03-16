import sys

g = 0

def outer(commands):
    n = 0

    def inner():
        nonlocal n
        global g
        for scope, value in commands:
            if scope == "global":
                g += value
            elif scope == "nonlocal":
                n += value
            elif scope == "local":
                x = 0
                x += value
    inner()
    return n

m = int(sys.stdin.readline())
commands = []
for _ in range(m):
    scope, value = sys.stdin.readline().split()
    commands.append((scope, int(value)))

n = outer(commands)

print(g, n)