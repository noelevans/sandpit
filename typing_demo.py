from typing import Literal

MODE = Literal['r', 'rb', 'w', 'wb']
def open_helper(file: str, mode: MODE) -> str:
  return 'something poinient'

open_helper('/some/path', 'r')
open_helper('/some/path', 'x')

