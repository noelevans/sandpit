import pdb
import atexit
import os
import readline
from pathlib import Path


class Config(pdb.DefaultConfig):
    just_my_code = True
    sticky_by_default = True

history_path = os.path.expanduser("~/.pdb_history")
Path(history_path).touch()

if os.path.getsize(history_path) > 100 * 1024:
    os.remove(history_path)

Path(history_path).touch()


def save_history(history_path=history_path):
    readline.write_history_file(history_path)


if os.path.exists(history_path):
    readline.read_history_file(history_path)

atexit.register(save_history, history_path=history_path)
