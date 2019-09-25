from pywinauto.keyboard import SendKeys

# List of keys available to send: http://pywinauto.readthedocs.io/en/latest/code/pywinauto.keyboard.html


# Opens program by sending keystrokes
def open_program(program):

    SendKeys('{LWIN}')
    SendKeys(program)
    SendKeys("{ENTER}")


if __name__ == "__main__":
    program = "discord"
    open_program(program)
