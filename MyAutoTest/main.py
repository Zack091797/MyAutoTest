# This is a sample Python script.
import re

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from selenium import webdriver

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    driver = webdriver.Chrome()
    driver.switch_to.parent_frame()
    driver.switch_to.alert
    driver.get_screenshot_as_png()
    # str = "$csv{apiname}"
    # result = re.findall("\\{(.*?)\\}", str)
    # print(result)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
