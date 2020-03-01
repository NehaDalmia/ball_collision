import cv2
import numpy as np
import math

def alter(x,y,m,special):
    if(-15<m<15):
            if(0<m<1 or -1<m<0):
                if(choice==0):
                    if(m>0):
                        y-=1
                        x+=1/m
                    if(m<0):
                        y+=1
                        x-=1/m
                if(choice==1):
                    if(m>0):
                        y+=1
                        x-=1/m
                    if(m<0):
                        y-=1
                        x+=1/m
            else:
                if(choice==0 ):
                    x+=1
                    if(m>=0):
                        y=y-(m*1)
                    else:
                        y=y-(m*1)+1
                elif(choice==1 ):   
                    x-=1
                    if(m>0):
                        y=y+(m*1)+1
                    else:
                        y=y+(m*1) 
    else:
        if(special==-1):
            y+=1
        else:
            y-=1
    return x,y
img = cv2.imread('one.png',cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_blur = cv2.medianBlur(gray, 5)
dst = cv2.Canny(gray, 50, 150,apertureSize=3)
#cv2.imshow('canny',dst)
#cv2.waitKey(10000)
height, width, channels = img.shape
circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, 10, param1=50, param2=10, minRadius=20, maxRadius=30)
a=[0,0,0,0]
lines=cv2.HoughLinesP(dst,1,np.pi/180,10,100,50)
lines=np.int64(np.around(lines))
cue=lines[0,0]
length=1000000
for i in range(0,len(lines)):
    for x1,y1,x2,y2 in lines[i]:
        d=((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
        if(d<length):
            length=d
            a[0]=x1
            a[1]=y1
            a[2]=x2
            a[3]=y2
choice=0
if circles is not None:
     circles = np.int64(np.around(circles))
     min=999999
     for i in circles[0, :]: 
        if(abs((i[0]-a[0])*(i[0]-a[0])+(i[1]-a[1])*(i[1]-a[1]))<min):  
            x=i
            min=abs((i[0]-a[0])*(i[0]-a[0])+(i[1]-a[1])*(i[1]-a[1]))
        elif(abs((i[0]-a[2])*(i[0]-a[2])+(i[1]-a[3])*(i[1]-a[3]))<min):
            x=i
            min=abs((i[0]-a[2])*(i[0]-a[2])+(i[1]-a[3])*(i[1]-a[3]))       
     m=(a[1]-a[3])/(a[2]-a[0])
     k=0
     special=-1
     if(a[0]>x[0]):
        choice=1
     
     while(True):
        for i in circles[0, :]: 
            if(np.array_equal(i,x)==False):
                cv2.circle(img, (i[0], i[1]), i[2], (0,0,255), -2)
            cv2.imshow("Result Image", img)
            cv2.waitKey(1)
            f=0
            z=(x[0]-i[0])*(x[0]-i[0])+(x[1]-i[1])*(x[1]-i[1])
            g=(x[2]+i[2])*(x[2]+i[2])
            if(g>z):
                temp=g
                g=z
                z=temp
                f=1
            if (0<math.fabs(z-g)<150 or 0<g<(x[2]+i[2])*(x[2]+i[2])-50): 
                
                if(i[0]!=x[0]) :
                    m=(x[1]-i[1])/(i[0]-x[0])
                else:
                    m=100
                if(i[0]>x[0]):
                    choice=0
                if(i[0]<x[0]):
                    choice=1
                if(m>12 or m<-12) :
                    if(x[1]>i[1]):
                        special =1
                    elif(x[1]<i[1]):
                        special=-1
                x=i
                for l in range(0,3):
                    cv2.circle(img, (x[0],x[1]), x[2], (0, 0, 0), -2)       
                    cv2.imshow("Result Image", img)
                    cv2.waitKey(1)
                    x[0],x[1]=alter(x[0],x[1],m,special)
                    cv2.circle(img, (x[0],x[1]), x[2], (255, 255, 255), -2)
        cv2.circle(img, (x[0],x[1]), x[2], (0, 0, 0), -2)
        k+=1
        if((x[1]-x[2])<=0):
            
            if(m>0):
                choice=0
            else:
                choice=1
            special*=-1
            m=m*-1
            x[0],x[1]=alter(x[0],x[1],m,special)
        if((x[0]-x[2])<=0):
            choice=0 
            m=m*-1
            x[0],x[1]=alter(x[0],x[1],m,special)
        if((width-x[0])-x[2]<=0):
            choice=1
            m=m*-1
            x[0],x[1]=alter(x[0],x[1],m,special)
        if((height-x[1])-x[2]<=0):
            if(m>0):
                choice=1
            else:
                choice=0
            m=m*-1
            special*=-1
            x[0],x[1]=alter(x[0],x[1],m,special)
        if(m>5 or -1< m<1):
            cv2.waitKey(10)
        if(k>20000):
            break
        cv2.imshow("Result Image", img)
        x[0],x[1]=alter(x[0],x[1],m,special)
        cv2.circle(img, (x[0],x[1]), x[2], (255, 255, 255), -2)
cv2.waitKey(0)
cv2.destroyAllWindows()