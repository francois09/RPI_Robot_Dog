#!/usr/bin/python

import time
import math
import smbus

# ============================================================================
# PCA9685 16-Channel LED Driver
# ============================================================================

class PCA9685:

  # Registers/etc.
  __MODE1              = 0x00
  __MODE2              = 0x01
  __SUBADR1            = 0x02
  __SUBADR2            = 0x03
  __SUBADR3            = 0x04
  __PRESCALE           = 0xFE
  __LED0_ON_L          = 0x06
  __LED0_ON_H          = 0x07
  __LED0_OFF_L         = 0x08
  __LED0_OFF_H         = 0x09
  __ALLLED_ON_L        = 0xFA
  __ALLLED_ON_H        = 0xFB
  __ALLLED_OFF_L       = 0xFC
  __ALLLED_OFF_H       = 0xFD

  # Mode 1 bits: (* = default)
  #  7 6 5 4 3 2 1 0
  #  | | | | | | | +--- AllCall led address (E0h) active/inactive (1*/0)
  #  | | | | | | +----- SubAddress 3 (E8h) active/inactive (1/0*)
  #  | | | | | +------- SubAddress 2 (E4h) active/inactive (1/0*) 
  #  | | | | +--------- SubAddress 1 (E2h) active/inactive  (1/0*)
  #  | | | +----------- Sleep (1*) or normal (0) mode
  #  | | +------------- Register Auto-increment (1) or no (0*)
  #  | +--------------- Use EXTCLK pin (1) or internal clock (0*)
  #  +----------------- Restart (1). 

  __MODE1_SLEEP = 0x10
  __MODE1_RESTART = 0x80

  # Mode 2 bits:
  # 7 6 5 4 3 2 1 0
  # | | | | | | | +---| OutNE: 00*, 01 or 1X manage the way LED out
  # | | | | | | +-----| is working. Check Datasheet for more infos
  # | | | | | +-------- Output LED mode: 0 = Open drain, 1* = Totem pole
  # | | | | +---------- OCH: Output change on STOP (0*) or ACK (1)
  # | | | +------------ Inverter: 0* normal or 1 inverted logic
  # +-+-+-------------- Reserved (0)

  __WAIT_CYCLE = 0.0005 # 500 µs
  __INTERNAL_CLOCK = 25000000.0 # 25 MHz
  __CYCLE_TICKS = 4096 # Nubmer of steps in a cycle

  def __init__(self, address):
    self.bus = smbus.SMBus(1)
    self.address = address
    # 
    # mode1 = self.read(self.__MODE1)
    # self.write(self.__MODE1, 0x00)

  def write(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    self.bus.write_byte_data(self.address, reg, value)

  def read(self, reg):
    "Read an unsigned byte from the I2C device"
    return self.bus.read_byte_data(self.address, reg)

  def bit_set(val, bitmask):
    return val |  bitmask

  def bit_clear(val, bitmask):
    return val & (0xFF - bitmask)

  def sleep(self):
    # If sleep mode is set without stopping PWM, Reset will raise
    mode = self.read(self.__MODE1)
    newmode = self.bit_set( self.bit_clear(mode, self.__MODE1_RESTART), self.__MODE1_SLEEP)
    self.write(self.__MODE1,newmode)
    return mode

  def wakeup(self):
    # To restart with previous PWM values
    mode = self.read(self.__MODE1)
    if (mode & self.__MODE1_RESTART ): # if restart is raised, unsleep and wait cycle
      self.write(self.__MODE1, self.bit_clear(mode, self.__MODE1_RESTART | self.__MODE1_SLEEP))
      time.sleep(self.__WAIT_CYCLE)
    # Then restart previous PWM values
    self.write( self.__MODE1, self.bit_set(mode, self.__MODE1_RESTART))
    return mode

  def setLED_duty(self, led, on, off):
    "Set on and off values for the nth led (0 to 15)"
    L_on  = on & 0xFF
    H_on  = (on >> 8) & 0x0F
    L_off = off & 0xFF
    H_off = (off >> 8) & 0x0F
    self.write(self.__LED0_ON_L+4*led, L_on)
    self.write(self.__LED0_ON_H+4*led, H_on)
    self.write(self.__LED0_OFF_L+4*led, L_off)
    self.write(self.__LED0_OFF_H+4*led, H_off)

  def setLED_ON(self, led):
    self.write(self.__LED0_ON_L+4*led, 0)
    self.write(self.__LED0_ON_H+4*led, 0x10)
    self.write(self.__LED0_OFF_L+4*led, 0)
    self.write(self.__LED0_OFF_H+4*led, 0)

  def setLED_OFF(self, led):
    self.write(self.__LED0_ON_L+4*led, 0)
    self.write(self.__LED0_ON_H+4*led, 0)
    self.write(self.__LED0_OFF_L+4*led, 0)
    self.write(self.__LED0_OFF_H+4*led, 0x10)

  def setPWMFreq(self, freq):
    "Sets the PWM Prescale based on frequency"
    prescaleval = self.__INTERNAL_CLOCK / ( self.__CYCLE_TICKS * float(freq))
    prescaleval -= 1.0

    # Set sleep mode before prescale set
    mode = self.sleep()
    self.write(self.__PRESCALE, int(math.floor(prescaleval + 0.5)))
    self.wakeup()

  # def setPWM(self, channel, on, off):
  #   "Sets a single PWM channel"
  #   self.write(self.__LED0_ON_L+4*channel, on & 0xFF)
  #   self.write(self.__LED0_ON_H+4*channel, on >> 8)
  #   self.write(self.__LED0_OFF_L+4*channel, off & 0xFF)
  #   self.write(self.__LED0_OFF_H+4*channel, off >> 8)

  # def setMotorPwm(self,channel,duty):
  #   self.setPWM(channel,0,duty)

  # def setServoPulse(self, channel, pulse):
  #   "Sets the Servo Pulse,The PWM frequency must be 50HZ"
  #   pulse = pulse*4096/20000        #PWM frequency is 50HZ,the period is 20000us
  #   self.setPWM(channel, 0, int(pulse))

if __name__=='__main__':
    pass
