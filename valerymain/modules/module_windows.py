from pywinauto.keyboard import SendKeys
import webbrowser
import time
import os
import ctypes

# user32.dll docs: http://www.webtropy.com/articles/art9-2.asp?lib=user32.dll
# Other windows api: http://www.webtropy.com/articles/Win32-API-DllImport-art9.asp?Windows+API | https://www.programcreek.com/python/example/53930/ctypes.windll.user32
# NOTE: I edited the source code from pywinauto to add my own modifier on lines 121 and 291 of keyboard.py
# This allows me to use the windows key as a modifier which holds the key down instead of pressing it.

# Query type source: https://stenevang.wordpress.com/2013/02/22/google-advanced-power-search-url-request-parameters/
GOOGLE_QUERY_TYPES = {"normal": "",
                      "images": "tbm=isch",
                      "books": "tbm=bks",
                      "videos": "tbm=vid",
                      "news": "tbm=nws",
                      "shopping": "tbm=shop",
                      "finance": "tbm=fin",
                      "flights": "tbm=flm",
                      "personal": "tbm=pers"}

# A dictionary that holds the file type as a key and a tuple with an application to open and a list of keys to press to
# open a new file in that application once it is open
# {"FILETYPE":("APPLICATION TO OPEN", [KEYS, TO, PRESS])}
# A "*_10" value in the key to press list represents a time to wait before hitting the next key, in this case 10 seconds
FILE_TYPES = {"word": ("word", ["*_3", "{ENTER}, {ENTER}"]),
              "powerpoint": ("powerpoint", ["*_3", "{ENTER}, {ENTER}"]),
              "spreadsheet": ("excel", ["*_3", "{ENTER}, {ENTER}"]),
              "excel": ("excel", ["*_3", "{ENTER}, {ENTER}"]),
              "photoshop": ("adobe photoshop", ["*_5", "^N", "*_1", "{ENTER}"]),
              "photo shop": ("adobe photoshop", ["*_5", "^N", "*_1", "{ENTER}"]),
              "illustrator": ("adobe illustrator", ["*_9", "^N", "*_4", "{ENTER}"]),
              "svg": ("adobe illustrator", ["*_9", "^N", "*_4", "{ENTER}"]),
              "audio": ("audacity", ("Audacity", [])),
              "email": ("mail", ["*_1", "{TAB}", "{TAB}", "{ENTER}"]),
              "text": ("notepad", [])
              }

# Holds prebuilt URLs for each specific website as well as the character the site uses to indicate a space between words (i.e. salad dressing = salad+dressing)
SEARCHABLE_WEBSITES = {
    "youtube": ("https://www.youtube.com/results?search_query=", "+"),
    "you tube": ("https://www.youtube.com/results?search_query=", "+"),
    "amazon": ("https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=", "+")
}

PROGRAMS_PATH = "interpreters\\interdepends\\programs"

# Get a list of all the programs in the program folder
program_list = os.listdir(PROGRAMS_PATH)

# Turn all the program names to lowercase
p2_list = [p.lower() for p in program_list]


# SIMPLE COMMANDS #
def paste_from_clipboard():
    SendKeys("^V")


# PROGRAM COMMANDS #


# Opens the windows menu, looks for an application and opens it
def open_application_v1(application):
    SendKeys("{VK_LWIN}")
    SendKeys(application + "{ENTER}")


# Searches for the passed in application in the application folder located at valerymain/interpreters/interdepends/programs
# Returns true if the application was found and opened, false if it wasn't
def open_application_v2(app):

    # Counter for index
    c = 0
    for string in p2_list:

        if app in string:

            # Create full path to app using counter
            path_to_file = PROGRAMS_PATH + "\\" + program_list[c]

            # Open the app
            os.startfile(path_to_file, "open")

            # Success
            return True

        else:
            c += 1

    # Failed to find the app in the folder
    return False


# Opens a new file in the application that creates the filetype passed | i.e. word opens new file in Microsoft Word
def open_new_file(filetype):

    print(filetype)

    # Unzipping data out of the dictionary
    app_to_open = FILE_TYPES[filetype][0]
    keys_to_send = FILE_TYPES[filetype][1]

    # Launches application
    open_application_v2(app_to_open)

    # For every key in the key to send list
    for key in keys_to_send:

        # If key to press is a wait signal (*_SOMETIME)
        if "*_" in key:
            # Separate the * and the number of seconds to sleep for, then sleep for that amount of time
            split_key = key.split("_")
            time.sleep(int(split_key[1]))

        else:
            SendKeys(key)


def close_window():
    SendKeys('%{F4}')


# Performs a simple ALT+TAB to return the focus on the application that was previously being used
def return_main_focus():

    # ALT+TAB
    SendKeys("%{VK_TAB}")


def minimize_all_windows():
    # Windows key hold down + M
    SendKeys("$M")


# POWER COMMANDS #


def lock_computer():
    # Locks computer
    # ctypes.windll.user32.LockWorkStation()
    ctypes.windll.user32.GetClipboardData()


def hibernate():

    # Open windows menu with power options WIN+X
    SendKeys("$X")

    # Navigate to hibernate option and select
    SendKeys("{VK_UP 2}{VK_RIGHT}{VK_DOWN}{ENTER}")


def shutdown():
    import os
    os.system("shutdown -s")

    # Shut down after X time
    # time = 10
    # os.system("shutdown /t %s " % str(time))

# BROWSER COMMANDS #


# Opens a new tab in the currently opened browser and searches google for the given query using the query type
# If no query type is given, a normal query (search) will occur | If main_focus is false it will refocus the previous window
def open_browser_search(query, query_type="normal", main_focus=False):

    url = "https://www.google.com/search?" + GOOGLE_QUERY_TYPES[query_type] + "&q=" + query
    webbrowser.open(url)

    if not main_focus:

        time.sleep(.5)

        # Returns the focus to main app
        return_main_focus()


# Opens the browser and searches a specific site for the query.
def open_browser_site_search(website, query, main_focus=False):

    # Replace spaces with whatever character the specific website uses to indicate a space in the URL query
    clean_query = query.replace(" ", SEARCHABLE_WEBSITES[website][1])

    # Attaches the query to the prebuilt URL from the SEARCHABLE_WEBSITES dictionary
    url = SEARCHABLE_WEBSITES[website][0] + clean_query

    webbrowser.open(url)


# TODO: Left off here:
# Ideas for grabbing links in the search (such as Valery, select the first link)
# 1.) Use selenium webdriver:https://stackoverflow.com/questions/8344776/can-selenium-interact-with-an-existing-browser-session
# 2.) Along with opening the query on the browser, open it using requests and scrape it as well?

