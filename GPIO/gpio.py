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


GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.HIGH)

GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.HIGH)

time.sleep(30) 

GPIO.cleanup()
p.stop()


