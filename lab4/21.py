import sys
import importlib

n = int(sys.stdin.readline())

for _ in range(n):
    module_path, attr = sys.stdin.readline().strip().split()

    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError:
        print("MODULE_NOT_FOUND")
        continue

    if not hasattr(module, attr):
        print("ATTRIBUTE_NOT_FOUND")
        continue

    value = getattr(module, attr)

    if callable(value):
        print("CALLABLE")
    else:
        print("VALUE")