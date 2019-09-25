from valerymain.modules import module_windows
from pywinauto.keyboard import SendKeys


# Minimizes all windows
def clear():
    module_windows.minimize_all_windows()


# Locks the computer
def lock():
    module_windows.lock_computer()


# Shuts computer down if correct passcode is given
def shutdown(passcode):
    if passcode == "1923":
        return 11


# Dictionary that holds all the functions in this script
function_dict = {"v clear": clear,
                 "v lock": lock,
                 "v shutdown": shutdown}

# Testing purposes, remove when not testing
if __name__ == "__main__":
    function_dict["clear"]()
