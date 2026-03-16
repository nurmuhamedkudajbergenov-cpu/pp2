import math

R = float(input())
x1,y1 = map(float,input().split())
x2,y2 = map(float,input().split())
dx,dy = x2-x1,y2-y1
L = math.sqrt(dx*dx+dy*dy)
if L==0:
    print(f"{0:.10f}")
else:
    t = (-x1*dx-y1*dy)/(L*L)
    cx,cy = x1+t*dx,y1+t*dy
    d2 = cx*cx+cy*cy
    if d2>R*R:
        print(f"{0:.10f}")
    else:
        h = math.sqrt(R*R-d2)
        t1=max(0.0,min(1.0,t-h/L))
        t2=max(0.0,min(1.0,t+h/L))
        print(f"{max(0.0,(t2-t1)*L):.10f}")