from ctypes import*
import time

# give location of dll
mydll = cdll.LoadLibrary("C:\\Users\\Nico\\Desktop\\LED_8.98\\LED\\Lib\\LogitechLedEnginesWrapper\\x64\\LogitechLedEnginesWrapper.dll")

# Color percentages to use
red = 80
green = 0
blue = 10

# Initialize library
mydll.LogiLedInit()

# Flash a single key
mydll.LogiLedFlashSingleKey(0x01, red, green, blue, 8000, 1000)

# Make the program sleep for as long as you want the lighting effect to happen
time.sleep(2)

# mydll.LogiLedRestoreLightingForKey('0x01')


# TODO: Link this to the .dll in this project and not the one on Desktop LUL
