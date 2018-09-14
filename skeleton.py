import RPi.GPIO as GPIO
import time
import Adafruit_MCP3008
import os
import Adafruit_GPIO.SPI as SPI

GPIO.setmode(GPIO.BCM)

switch1 = 21
switch2 = 16
switch3 = 12

GPIO.setup(switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch3, GPIO.IN, pull_up_down=GPIO.PUD_UP)



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

#def one(channel):

#def two(channel):
    
#def three(channel):

#while(1):
#    GPIO.add_event_detect(switch1, GPIO.FALLING, callback=one, bouncetime=300)
#    GPIO.add_event_detect(switch2, GPIO.FALLING, callback=two, bouncetime=300)
#    GPIO.add_event_detect(switch3, GPIO.FALLING, callback=three, bouncetime=300)

def ConvertVolts(data,places):
 volts = (data * 3.3) / float(1023)
 volts = round(volts,places)
 return volts

print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} |'.format(*range(8)))
print('-' * 57)
# Main program loop.
while True:
    values = [0]*3
    #for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
    pot_data = mcp.read_adc(0)
    values[0] = ConvertVolts(pot_data,2)
     
    temperature_data = mcp.read_adc(1) #Temperature
    values[1] = int(0.3921*temperature_data - 60.891)  #Excel linear approximation
    
    ldr_data = mcp.read_adc(2)
    values[2] = int(0.11*ldr_data - 2.3102)
    
    
    
     #values[i] = mcp.read_adc(i)
    # Print the ADC values.
    print('| {0:>4} | {1:>4} C | {2:>4}% |'.format(*values))
    # Pause for half a second.
    time.sleep(0.5)






