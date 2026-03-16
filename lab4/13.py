import json,re

def get(data, q):
    try:
        for t in re.findall(r'[^\.\[\]]+|\[\d+\]', q):
            data = data[int(t[1:-1])] if t[0]=='[' else data[t]
        return json.dumps(data,separators=(',',':'))
    except:
        return 'NOT_FOUND'

d = json.loads(input())
for _ in range(int(input())):
    print(get(d, input()))