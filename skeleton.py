import RPi.GPIO as GPIO
import time
import Adafruit_MCP3008
import os
import Adafruit_GPIO.SPI as SPI

#GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

switch1 = 21
switch2 = 16
switch3 = 12
switch4 = 20

GPIO.setup(switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch4, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Software SPI configuration:
SPICLK  = 18
SPIMISO = 23
SPIMOSI = 24
SPICS   = 25

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, miso=SPIMISO, mosi=SPIMOSI)

#Variables
frequency = 0.5

h = 0
m = 0
s = 0

list = []

Bool = True

def one(channel):
    timer = str(0)+":"+str(0)+":"+str(0)   #reset timer
    os.system('printf "\033c"')   #clear

def two(channel):     #Swicthes frequency
    global frequency
    if (frequency == 0.5):
        frequency = 1
    elif (frequency == 1):
        frequency = 2
    elif (frequency == 2):
        frequency = 0.5    #resets to 0.5s frequency
    
def three(channel):  #Toggle stop and start
    global Bool
    if Bool == True:
        Bool = False
    else:
        Bool = True
        
def four(channel):
    print("")
    print('-' * 47)
    print('|   Time   |   Timer  |  Pot   | Temp  | Light|')
    print('-' * 47)
    print('| '+str(list[0][0])+' | '+str(list[0][1])+' |  '+str(list[0][2])+' C |   '+str(list[0][3])+'% |   '+str(list[0][4])+' |')
    print('-' * 47)
    print('| '+str(list[1][0])+' | '+str(list[1][1])+' |  '+str(list[1][2])+' C |   '+str(list[1][3])+'% |   '+str(list[1][4])+' |')
    print('-' * 47)
    print('| '+str(list[2][0])+' | '+str(list[2][1])+' |  '+str(list[2][2])+' C |   '+str(list[2][3])+'% |   '+str(list[2][4])+' |')
    print('-' * 47)
    print('| '+str(list[3][0])+' | '+str(list[3][1])+' |  '+str(list[3][2])+' C |   '+str(list[3][3])+'% |   '+str(list[3][4])+' |')
    print('-' * 47)
    print('| '+str(list[4][0])+' | '+str(list[4][1])+' |  '+str(list[4][2])+' C |   '+str(list[4][3])+'% |   '+str(list[4][4])+' |')
    print('-' * 47)
    print(' ')

GPIO.add_event_detect(switch1, GPIO.FALLING, callback=one, bouncetime=300)
GPIO.add_event_detect(switch2, GPIO.FALLING, callback=two, bouncetime=300)
GPIO.add_event_detect(switch3, GPIO.FALLING, callback=three, bouncetime=300)
GPIO.add_event_detect(switch4, GPIO.FALLING, callback=four, bouncetime=300)

try:

    def ConvertVolts(data,places):
        volts = (data * 3.3) / float(1023)
        volts = round(volts,places)
        return volts

    # Print nice channel column headers.
    print('|   Time   |   Timer  |  Pot   | Temp  | Light|')
    print('-' * 47)
    # Main program loop.
    while True:

        values = [0]*5
        #for i in range(8):
        # The read_adc function will get the value of the specified channel (0-2).
        pot_data = mcp.read_adc(0)
        values[2] = ConvertVolts(pot_data,2)
     
        temperature_data = mcp.read_adc(1) #Temperature
        values[3] = int(0.3921*temperature_data - 60.891)  #Excel linear approximation
    
        ldr_data = mcp.read_adc(2)
        values[4] = int(0.11*ldr_data - 2.3102)
    
        hour = time.strftime("%H")
        min = time.strftime("%M")
        sec = time.strftime("%S")
    
        values[0] = hour+":"+min+":"+sec
        
        if s > 59:
            s = 0
            m+=1
        elif m > 59:
            h+=1
            m = 0
        else:
            s+=frequency
    
        timer = str('%02d'%h)+":"+str('%02d'%m)+":"+str('%02d'%int(s))
        values[1] = timer
        
        if Bool == False:
            list.append([values[0], values[1], values[2], values[3], values[4]])
        
        if Bool == True:
            print('| {0:>4} | {1:>4} | {2:>4} C | {3:>4}% | {4:>4} |'.format(*values))
            print('-' * 47)
        # Pause for frequency seconds.
        time.sleep(frequency)

except KeyboardInterrupt:
    GPIO.cleanup() # clean up GPIO on CTRL+C exit
        



