from datetime import datetime,timezone,timedelta

def p(s):
    d,t,z = s.split()
    sign = 1 if '+' in z else -1
    h,m = map(int,z.replace('UTC+','').replace('UTC-','').split(':'))
    dt = datetime.strptime(d+' '+t,'%Y-%m-%d %H:%M:%S')
    return datetime(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second,tzinfo=timezone(timedelta(hours=sign*h,minutes=sign*m)))

a,b = p(input()),p(input())
print(int((b-a).total_seconds()))