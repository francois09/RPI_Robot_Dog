#!/usr/bin/python

from PCA9685 import PCA9685

# ============================================================================
# Servo board Driver
#
# This implement usage of a PCA9685 LED controller into a PWM servo motor
# driver. Specific for RobotDog kit
# ============================================================================

class ServoBoard:

    # Values hardware coded
    __PCA_ADDRESS = 0x40

    def __init__(self):
        self.pca = PCA9685(__PCA_ADDRESS)

if __name__=='__main__':
    pass
