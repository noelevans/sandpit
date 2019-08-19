"""

Start a nvim with this command:
    $ NVIM_LISTEN_ADDRESS=/tmp/nvim nvim

And then run these python commands:

"""

from pynvim import attach


nvim = attach('socket', path='/tmp/nvim')
print(nvim.buffer.current.name)

