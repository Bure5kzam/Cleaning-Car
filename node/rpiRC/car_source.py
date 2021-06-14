import sys 
sys.path.append('./Raspi-MotorHAT-python3') 
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor 
from Raspi_PWM_Servo_Driver import PWM 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5 import QtSql 
import atexit 
import time 

import RPi.GPIO as GPIO
import picamera
import time

# camera = picamera.PiCamera()
# camera.resolution = (2592, 1944) 

# time.sleep(3)
# camera.capture('snapshot.jpg')

GPIO.setmode(GPIO.BCM)
 
GPIO_TRIGGER = 15
GPIO_ECHO = 14
elapsed = 0

GPIO.setup(GPIO_TRIGGER,GPIO.OUT) 
GPIO.setup(GPIO_ECHO,GPIO.IN)
 

class pollingThread(QThread): 
  def __init__(self): 
    super().__init__() 

  def run(self):     
    self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL') 
    self.db.setHostName("3.35.8.78")         
    self.db.setDatabaseName("DB_15_04") 
    self.db.setUserName("SSAFY15_04_1") 
    self.db.setPassword("1234")
    ok = self.db.open() 
    print(오케이)   

    self.mh = Raspi_MotorHAT(addr=0x6f)
    self.myMotor = self.mh.getMotor(2) 
    self.myMotor.setSpeed(100) 
            
    self.pwm = PWM(0x6F) 
    self.pwm.setPWMFreq(60) 
    global elapsed

    self.auto = 0
    self.getQuery() 

  def getQuery(self): 
    while True: 
      time.sleep(0.01) 
      query = QtSql.QSqlQuery("select * from command_01 order by time desc limit 1"); 
      query.next() 
      cmdTime = query.record().value(0) 
      cmdType = query.record().value(1) 
      cmdArg = query.record().value(2) 
      is_finish = query.record().value(3) 
             
      if is_finish == 0 : 
        #detect new command 
        print(cmdTime.toString(), cmdType, cmdArg) 

        #update 
        query = QtSql.QSqlQuery("update command_01 set is_finish=1 where is_finish=0"); 
        #motor 
        if cmdType == "auto_on" : 
          print("Auto on")
          self.myMotor.setSpeed(70)
          self.middle()
          self.myMotor.run(Raspi_MotorHAT.FORWARD)
          self.auto = 1
        if cmdType == "auto_off" : 
          print("Auto off")
          self.auto = 0
          self.middle()
          self.myMotor.run(Raspi_MotorHAT.RELEASE)

        if self.auto == 0 :
          if cmdType == "go": self.go()         
          if cmdType == "back": self.back() 
          if cmdType == "left": self.left() 
          if cmdType == "right": self.right() 
          if cmdType == "mid": self.middle()

      if self.auto == 1 :       
        if elapsed < 0.001:
          print("warning : ", elapsed)
          self.myMotor.setSpeed(70)
          self.myMotor.run(Raspi_MotorHAT.BACKWARD)
          time.sleep(1)
          self.myMotor.run(Raspi_MotorHAT.FORWARD)
          self.right()
          time.sleep(3)
          self.middle()
        else:
          self.myMotor.setSpeed(70)
          self.myMotor.run(Raspi_MotorHAT.FORWARD)

  def go(self): 
    print("MOTOR GO") 
    self.myMotor.setSpeed(100)  
    self.myMotor.run(Raspi_MotorHAT.BACKWARD) 
    #time.sleep(1) 
    #self.myMotor.run(Raspi_MotorHAT.RELEASE) 
  def back(self): 
    print("MOTOR BACK") 
    #self.myMotor.run(Raspi_MotorHAT.FORWARD) 
    self.myMotor.run(Raspi_MotorHAT.RELEASE) 
  def left(self): 
    print("MOTOR LEFT") 
    self.pwm.setPWM(0, 0, 150); 
  def right(self): 
    print("MOTOR RIGHT") 
    self.pwm.setPWM(0, 0, 430); 
  def middle(self): 
    print("MOTOR MIDDLE") 
    self.pwm.setPWM(0, 0, 350); 
class sensingThread(QThread):
    def __init__(self):
        super().__init__()
    def run(self):
        try:
            global elapsed
            while True:
                stop = 0
                start = 0
                GPIO.output(GPIO_TRIGGER, False)
                time.sleep(1)
         
                GPIO.output(GPIO_TRIGGER, True)
                time.sleep(0.00001)
                GPIO.output(GPIO_TRIGGER, False)
                
                while GPIO.input(GPIO_ECHO)==0:
                    start = time.time()
         
                while GPIO.input(GPIO_ECHO)==1:

                    stop = time.time()
         
                # Calculate pulse length
                elapsed = stop-start
         
                if (stop and start):
                    distance = (elapsed * 34000.0) / 2
                    #print ("Distance : %.1f cm" % distance)
        except KeyboardInterrupt:   
            print ("Ultrasonic Distance Measurement End" )
            GPIO.cleanup()

th = pollingThread()
th.start()
th2 = sensingThread()
th2.start()
app = QApplication([]) 


#infinity loop 
while True:  
  pass
