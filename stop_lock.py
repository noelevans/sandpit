import datetime
import pyautogui
import sys
import time


"""
Simulate keyboard actions to prevent a screensaver /
screenlock from activating on a computer
"""

now = datetime.datetime.now
start_time = now()


def act():
    pyautogui.press("down")
    time.sleep(0.5)
    pyautogui.press("down")
    time.sleep(0.5)


def main():
    run_mins = len(sys.argv) > 1 and int(sys.argv[1]) or 16 * 60
    while now() < start_time + datetime.timedelta(minutes=run_mins):
        for _ in range(3):
            act()
        print(".")

        time.sleep(20)


if __name__ == "__main__":
    main()
