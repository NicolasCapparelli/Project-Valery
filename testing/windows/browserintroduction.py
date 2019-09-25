import webbrowser

# Documentation: https://docs.python.org/3.3/library/webbrowser.html
# Ability to open in new window, new tab, etc... all in docs


# Opens URL with default windows
def open_with_default(url):
    webbrowser.open(url, autoraise=False)


# Opens URL with a specific windows given the path to the windows executable
def open_with_specific(url):

    # MacOS
    # chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

    # Windows
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

    # Linux
    # chrome_path = '/usr/bin/google-chrome %s'

    webbrowser.get(chrome_path).open(url)


if __name__ == "__main__":
    URL = 'http://www.amazon.com'

    open_with_default(URL)
    # open_with_specific(URL)


