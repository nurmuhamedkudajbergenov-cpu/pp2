from datetime import datetime,timezone,timedelta

def p(s):
    d,z = s.split()
    sign = 1 if '+' in z else -1
    h,m = map(int,z.replace('UTC+','').replace('UTC-','').split(':'))
    dt = datetime.strptime(d,'%Y-%m-%d')
    return datetime(dt.year,dt.month,dt.day,tzinfo=timezone(timedelta(hours=sign*h,minutes=sign*m)))

a,b = p(input()),p(input())
print(int(abs((a-b).total_seconds())//86400))