import datetime
import time
import win32api
import win32con

from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener


"""
Simulate keyboard actions to prevent a screensaver /
screenlock from activating on a computer
"""

now = datetime.datetime.now

last_move = now()
start_time = now()


def on_move(x, y):
    last_move = now()
    print('m')


def act():
    win32api.keybd_event(0x28, 0, 0, 0)
    time.sleep(0.5)
    win32api.keybd_event(0x28, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.5)


def main():
    with MouseListener( on_move=on_move,) as mouse_listener:
        mouse_listener.join()
    with KeyboardListener( on_move=on_move,) as keyboard_listener:
        keyboard_listener.join()
    while now() < start_time + datetime.timedelta(hours=16):
        if (now() - last_move).seconds > 120:
            act()
            print('.')

        time.sleep(20)


if __name__ == '__main__':
    main()
