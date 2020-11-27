import RPi.GPIO as GPIO

import time

GPIO.setwarnings(False)
R, G, B = 11, 12, 13
GPIO.setmode(GPIO.BOARD)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
pwmR = GPIO.PWM(R, 100)
pwmG = GPIO.PWM(G, 100)
pwmB = GPIO.PWM(B, 100)
pwmR.start(0)
pwmG.start(0)
pwmB.start(0)
t = 10
# 红灯，绿灯，蓝灯全亮（白色）
pwmR.ChangeDutyCycle(100)
pwmG.ChangeDutyCycle(100)
pwmB.ChangeDutyCycle(100)
time.sleep(t)
pwmR.stop()
pwmG.stop()
pwmB.stop()
GPIO.cleanup()
