#
# Show progress state with leds

import time
from Led import *
led=Led()

def Led_fetch():
    try:
        # Red wipe
        led.colorWipe([127,0,0])
    except KeyboardInterrupt:
        led.colorWipe([0, 0, 0])   #turn off the light

def Led_pull():
    try:
        # Blue wipe
        led.colorWipe([0,0,127])
    except KeyboardInterrupt:
        led.colorWipe([0, 0, 0])   #turn off the light

def Led_start():
    try:
        # Green wipe
        led.colorWipe([0,127,0])
    except KeyboardInterrupt:
        led.colorWipe([0, 0, 0])   #turn off the light

def test_Led():
    try:
        #Red wipe
        print ("\nRed wipe")
        led.colorWipe([255, 0, 0]) 
        time.sleep(1)

        #Green wipe
        print ("\nGreen wipe")
        led.colorWipe([0, 255, 0]) 
        time.sleep(1)

        #Blue wipe
        print ("\nBlue wipe")
        led.colorWipe([0, 0, 255]) 
        time.sleep(1)

        #White wipe
        print ("\nWhite wipe")
        led.colorWipe([255, 255, 255]) 
        time.sleep(1)
    
        led.colorWipe([0, 0, 0])   #turn off the light
        print ("\nEnd of program")
    except KeyboardInterrupt:
        led.colorWipe([0, 0, 0])   #turn off the light
        print ("\nEnd of program")

        
from ADS7830 import *
adc=ADS7830()
def test_Adc():
    try:
        while True:
            Power=adc.readAdc(0)/255.0*5.0*3
            print ("The battery voltage is "+str(Power)+"V")
            time.sleep(1)
            print ('\n')
    except KeyboardInterrupt:
        print ("\nEnd of program")

# Main program logic follows:
if __name__ == '__main__':

    print ('Process is starting ... ')
    import sys
    if len(sys.argv)<2:
        print ("Parameter error: Please assign the device")
        exit() 
    if sys.argv[1] == 'fetch':
        Led_fetch()
    if sys.argv[1] == 'pull':
        Led_pull()
    if sys.argv[1] == 'start':
        Led_start()
