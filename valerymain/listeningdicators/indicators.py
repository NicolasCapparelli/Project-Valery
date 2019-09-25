from ctypes import cdll
from valerymain.listeningdicators import LogitechLEDKeys
import time
import math

# Constants
# valery_color_percent = (74, 50, 100)
valery_color_percent = (100, 0, 0)
logitech_dll = cdll.LoadLibrary("listeningdicators\\LogitechLedEnginesWrapper.dll")


# Converts regular rgb to a percent of each color needed. Must be done if passing an RBG color to the Logitech LED library
def rgb_to_percent(rgb_tuple):

    new_color = []

    for color in rgb_tuple:
        new_color.append(math.floor(color / 255))

    return tuple(new_color)


# Makes the keyboard pulse a color. color: RGB_Percent tuple | duration: int seconds | interval: int milliseconds
def logitech_pulse_keyboard(color=valery_color_percent, duration=0, interval=1000):

    # dll function call with passed in parameters
    logitech_dll.LogiLedPulseLighting(color[0], color[1], color[2], duration*1000, interval)

    logitech_dll.LogiLedStopEffects()


# Makes the keyboard flash a color. Same parameters as logitech_pulse_keyboard()
def logitech_flash_keyboard(color=valery_color_percent, duration=2, interval=500):

    logitech_dll.LogiLedFlashLighting(color[0], color[1], color[2], duration*1000, interval)


# Flashes a single key with the given color
def logitech_flash_key(keyname=LogitechLEDKeys.G_LOGO, color=valery_color_percent):

    # Saves the previous lighting effect for the key we are about to change
    logitech_dll.LogiLedSaveLightingForKey(keyname)

    # dll function call with the passed in parameters to achieve flashing effect
    logitech_dll.LogiLedSetLightingForKeyWithKeyName(keyname, color[0], color[1], color[2])


def start():
    logitech_dll.LogiLedInit()


def stop():
    # logitech_dll.LogiLedRestoreLighting()
    logitech_dll.LogiLedShutdown()
    # logitech_dll.LogiLedInit()


INDICATORS = {"lt_pulse_keyboard": logitech_pulse_keyboard,
              "lt_flash_keyboard": logitech_flash_keyboard,
              "lt_flash_key": logitech_flash_key,
              "stop": stop
              }

# TODO: Pick a more vibrant color for valery
# TODO: Make all paths relative to working directory: 'C:\Users\Nico\PycharmProjects\project-valery\valerymain'
