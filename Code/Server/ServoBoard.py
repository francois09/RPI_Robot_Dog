#!/usr/bin/python

from PCA9685 import PCA9685
import time

# ============================================================================
# Servo board Driver
#
# This implement usage of a PCA9685 LED controller into a PWM servo motor
# driver. Specific for RobotDog kit
# ============================================================================

# Servo list:
#
# Head: 15
# Front right: 11, 12, 13
# Rear right: 8, 9, 10
# Front left: 4, 3, 2
# Rear left: 7, 6, 5

# Unused: 0,1,14

class ServoBoard:

    # Values hardware coded
    __PCA_ADDRESS = 0x40
    __PCA_FREQ = 50

    def __init__(self):
        self.pca = PCA9685(self.__PCA_ADDRESS)
        self.pca.setPWMFreq(self.__PCA_FREQ)
        self.angleMin=18
        self.angleMax=162

    def remap(self, val, From, To):
        "Remap val from From interval to To inverval"
        return (To[1]-To[0])*(val-From[0]) / (From[1]-From[0]) + To[0]

    def setServoAngle(self,chan,angle)
      if angle < self.angleMin:
          angle = self.angleMin
      elif angle > self.angleMax:
          angle = self.angleMax
      val=self.remap(angle, [0,180], [102,512])
      self.pca.setLED_duty(chan, 0, int(val))

if __name__=='__main__':
    while True:
      try:
        self.setServoAngle(13,90)
        timesleep(1)
        self.setServoAngle(13,80)
        timesleep(0.5)
        self.setServoAngle(13,90)
        timesleep(0.5)
        self.setServoAngle(13,100)
        timesleep(0.5)

      except KeyboardInterrupt:
          print ("\nEnd test\n")
          break
    pass
