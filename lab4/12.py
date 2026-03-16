import json

def diff(a, b, path=''):
    res = []
    for k in set(list(a)+list(b)):
        p = (path+'.'+k).lstrip('.')
        if k not in a:
            res.append(f"{p} : <missing> -> {json.dumps(b[k],separators=(',',':'))}")
        elif k not in b:
            res.append(f"{p} : {json.dumps(a[k],separators=(',',':'))} -> <missing>")
        elif isinstance(a[k],dict) and isinstance(b[k],dict):
            res+=diff(a[k],b[k],p)
        elif a[k]!=b[k]:
            res.append(f"{p} : {json.dumps(a[k],separators=(',',':'))} -> {json.dumps(b[k],separators=(',',':'))}")
    return res

a,b = json.loads(input()),json.loads(input())
out = sorted(diff(a,b))
print('\n'.join(out) if out else 'No differences')