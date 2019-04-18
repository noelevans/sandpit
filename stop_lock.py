import datetime
import time
import win32api
import win32con


"""
Simulate keyboard actions to prevent a screensaver /
screenlock from activating on a computer
"""

now = datetime.datetime.now
start_time = now()

def act():
    win32api.keybd_event(0x28, 0, 0, 0)
    time.sleep(0.5)
    win32api.keybd_event(0x28, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.5)


def main():
    while now() < start_time + datetime.timedelta(hours=16):
        for _ in range(3):
            act()
        print('.')

        time.sleep(20)


if __name__ == '__main__':
    main()
