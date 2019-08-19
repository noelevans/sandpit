" generate a random integer from range [Low, High] using Python
function! RandInt(Low, High) abort
" if you use Python 3, the python block should start with `python3` instead of
" `python`, see https://github.com/neovim/neovim/issues/9927
python3 << EOF
import vim
import random

# using vim.eval to import variable outside Python script to python
idx = random.randint(int(vim.eval('a:Low')), int(vim.eval('a:High')))

# using vim.command to export variable inside Python script to vim script so
# we can return its value in vim script
vim.command("let index = {}".format(idx))
EOF

return index
endfunction
