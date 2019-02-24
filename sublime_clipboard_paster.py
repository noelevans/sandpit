import ctypes
import re
import sublime
import sublime_plugin
import sys


"""
ln -s sublime_clipboard_paster.py
    /home/noel/.config/sublime-text-3/Packages/User/paster.py
"""

class PasterCommand(sublime_plugin.TextCommand):

    def windows_get_clipboard(self):
        CF_TEXT = 1
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32

        user32.OpenClipboard(0)
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked).value
            kernel32.GlobalUnlock(data_locked)
        else:
            text = 'No text in clipboard'

        user32.CloseClipboard()

        text = text.decode(errors='ignore')
        crufts = ['<0x0d>', '\\r']
        for cruft in crufts:
            text = text.replace(cruft, '')


    def linux_get_clipboard(self):
        import clipboard
        return clipboard.paste()


    def run(self, edit):
        if sys.platform == 'win32':
            text = self.windows_get_clipboard()
        else:
            text = self.linux_get_clipboard()
        text = re.sub(r'^Latest.stories.*^See.more', '', text, flags=re.DOTALL)
        self.view.insert(edit, 0, '\n' + text)

