import cv2
import numpy as np
import imutils
from imutils.video import VideoStream
from imutils.video import FPS
import time

import RPi.GPIO as GPIO

in1=24
in2=23
enA=25

in3=27
in4=17
enB=22

GPIO.setmode(GPIO.BCM)

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)


p=GPIO.PWM(enA,1000)
p.start(100)

q=GPIO.PWM(enB,1000)
q.start(100)


vs=VideoStream(usePiCamera=True).start()
time.sleep(2)

fps=FPS().start()

while True:
   
    
    frame=vs.read()
    frame=imutils.resize(frame,width=500)
    h,w=frame.shape[0:2]
    xcenter=w/2
    center=(w/2,h/2)
    
    M=cv2.getRotationMatrix2D(center,180,1.0)
    frame=cv2.warpAffine(frame,M,(w,h))
    
    
    
    hsv_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    lower_color=np.array([0, 100,150],dtype='uint8')
    upper_color=np.array([30,255,255],dtype='uint8')
    
    mask=cv2.inRange(hsv_frame,lower_color,upper_color)
    
    # in opencv 3 findContours returns a tuple: image,contours,hierarchy
    contours=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
    
    gx,gy=0,0
    
    for contour in contours:
        if cv2.contourArea(contour)>100:
            x,y,w,h =cv2.boundingRect(contour)
            gx=x+w/2
            gy=y+h/2
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)    
   
    cv2.imshow('detection',frame)
    
    if cv2.waitKey(1)&0xFF==ord('q'):
        cv2.destroyAllWindows()
        vs.stop()
        break
    
    if gx==0:
        #stop
        print('stop')
        
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in1,GPIO.LOW)
        
        
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
    else:
        if gx>xcenter+100:
             #yaw right
            p.ChangeDutyCycle(80)
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            
            q.ChangeDutyCycle(0)
            GPIO.output(in4,GPIO.HIGH)
            GPIO.output(in3,GPIO.LOW)
            print('yaw right')
        elif gx<xcenter-100:
            #yaw left
            p.ChangeDutyCycle(0)
            GPIO.output(in2,GPIO.HIGH)
            GPIO.output(in1,GPIO.LOW)
            
            q.ChangeDutyCycle(80)
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)
            
            print('yaw left')
        else:
            #move straight
            p.ChangeDutyCycle(70)
            GPIO.output(in2,GPIO.HIGH)
            GPIO.output(in1,GPIO.LOW)
            
            q.ChangeDutyCycle(70)
            GPIO.output(in4,GPIO.HIGH)
            GPIO.output(in3,GPIO.LOW)
            print('move sraight')
        
    fps.update()
    
    
    
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
     
