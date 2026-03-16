import json

def patch(s, p):
    for k, v in p.items():
        if v is None:
            s.pop(k, None)
        elif isinstance(v, dict) and isinstance(s.get(k), dict):
            patch(s[k], v)
        else:
            s[k] = v
    return s

s = json.loads(input())
p = json.loads(input())
print(json.dumps(patch(s, p), sort_keys=True, separators=(',',':')))