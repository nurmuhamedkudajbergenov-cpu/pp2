from datetime import datetime,timezone,timedelta
import math

def p(s):
    d,z = s.split()
    sign = 1 if '+' in z else -1
    h,m = map(int,z.replace('UTC+','').replace('UTC-','').split(':'))
    dt = datetime.strptime(d,'%Y-%m-%d')
    return datetime(dt.year,dt.month,dt.day,tzinfo=timezone(timedelta(hours=sign*h,minutes=sign*m)))

def leap(y): return y%4==0 and(y%100!=0 or y%400==0)

birth,now = p(input()),p(input())
bm,bd = birth.month,birth.day
for y in [now.year,now.year+1]:
    bd2 = 28 if bm==2 and bd==29 and not leap(y) else bd
    c = datetime(y,bm,bd2,tzinfo=birth.tzinfo)
    d = (c-now).total_seconds()
    if d>=0:
        print(math.ceil(d/86400))
        break