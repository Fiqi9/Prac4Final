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







