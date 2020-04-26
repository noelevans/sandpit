if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

call plug#begin('~/.vim/plugged')

Plug 'tpope/vim-fugitive'     " Git tools
Plug 'tpope/vim-surround'
Plug 'tpope/vim-commentary'
Plug 'itchyny/lightline.vim'
Plug 'airblade/vim-gitgutter'
" Plug 'mhinz/vim-startify'
Plug 'sjl/gundo.vim'
Plug 'alfredodeza/pytest.vim'
" Plug 'w0rp/ale'
" Plug 'jpalardy/vim-slime'      " Copying code to another tmux pane for repl interaction
Plug 'neoclide/coc.nvim', {'branch': 'release', 'do': ':CocInstall coc-python'}
Plug 'nanotech/jellybeans.vim'
" Plug 'kalekundert/vim-coiled-snake'
Plug 'xolox/vim-misc'            " Dependency of vim-session
Plug 'xolox/vim-session'
Plug 'ntpeters/vim-better-whitespace'
Plug 'rrethy/vim-illuminate'
Plug 'mileszs/ack.vim'
" Plug 'liuchengxu/vista.vim'
Plug 'majutsushi/tagbar'
Plug 'psf/black'
" Plug 'junegunn/fzf.vim'

call plug#end()

filetype on

" Sets how many lines of history VIM has to remember
set history=500

" Set to auto read when a file is changed from the outside
set autoread
set autowrite

" Set 7 lines to the cursor - when moving vertically using j/k
set so=7

let $LANG='en'
set langmenu=en

" Turn on the Wild menu
set wildmode=longest,list
set wildmenu

"Always show current position
set ruler
set hidden
set ignorecase
set smartcase
set hlsearch
set incsearch

" Don't redraw while executing macros (good performance config)
set lazyredraw

" Show matching brackets under cursor
set showmatch

" Tenths of second to blink when matching brackets
set mat=2

set noerrorbells
set novisualbell
set t_vb=

set path+=**
set tags=tags
set showcmd
set undofile     " Persistent undo
set number
set relativenumber
set splitright
set splitbelow

" Allows you to do 'gf' on config which opens config.py
set suffixesadd=.py

" Add a bit extra margin to the left
" set foldcolumn=1

set encoding=utf8

" Use Unix as the standard file type
set ffs=unix,dos,mac

" Use spaces instead of tabs
set expandtab

" 1 tab == 4 spaces
set shiftwidth=4
set tabstop=4

set ai "Auto indent
set wrap "Wrap lines
set clipboard+=unnamedplus

let g:ale_enabled = 0

" Ignore compiled files
set wildignore=*.o,*~,*.pyc
if has("win16") || has("win32")
    set wildignore+=.git\*,.hg\*,.svn\*
else
    set wildignore+=*/.git/*,*/.hg/*,*/.svn/*,*/.DS_Store
endif

" hi CursorLine term=bold cterm=bold guibg=Grey40
hi link illuminatedWord Visual

" Enable syntax highlighting
syntax enable

" Mark lines going past 80 characters
augroup vimrc_autocmds
  autocmd BufEnter * highlight OverLength ctermbg=darkgrey guibg=#111111
  autocmd BufEnter * match OverLength /\%80v.*/
augroup END

autocmd BufWritePost *.py execute ':Black'

" Backup settings from
" https://begriffs.com/posts/2019-07-19-history-use-vim.html?hn=3

" Protect changes between writes. Default values of
" updatecount (200 keystrokes) and updatetime
" (4 seconds) are fine
set swapfile
set directory^=~/.vim/swap//

" protect against crash-during-write
set writebackup
" but do not persist backup after successful write
set nobackup
" use rename-and-write-new method whenever safe
set backupcopy=auto
" patch required to honor double slash at end
if has("patch-8.1.0251")
	" consolidate the writebackups -- not a big
		" deal either way, since they usually get deleted
			set backupdir^=~/.vim/backup//
			end
" persist the undo tree for each file
set undofile
set undodir^=~/.vim/undo//


noremap <Up> <Nop>
noremap <Down> <Nop>
noremap <Left> <Nop>
noremap <Right> <Nop>
noremap <PageUp> <Nop>
noremap <PageDown> <Nop>


nnoremap <Left> :bprevious<CR>
nnoremap <Right> :bnext<CR>
nnoremap <C-Left> :cprevious<CR>
nnoremap <C-Right> :cnext<CR>

imap hh <Esc>

let mapleader="\<Space>"

" :W sudo saves the file
" (useful for handling the permission-denied error)
"command W w !sudo tee % > /dev/null

" Correct spelling error on this line with first dictionary choice
"nnoremap <leader>sp :normal! mf[s1z=`f<cr>
" or...
function! FixLastSpellingError()
    normal! mf[s1z=`f
endfunction
nnoremap <leader>sp :call FixLastSpellingError()<cr>

fun! TrimWhitespace()
    let l:save = winsaveview()
    keeppatterns %s/\s\+$//e
    call winrestview(l:save)
endfun
nnoremap <leader>wspace :call TrimWhitespace()<cr>

" Toggle spell checking
map <leader>ss :setlocal spell!<cr>

nnoremap <leader>sop :source %<cr>
" nnoremap <leader>h :set hlsearch!<cr>
nnoremap <leader>h :nohlsearch<cr>
nnoremap <leader>lint :ALEToggle<cr>
nnoremap <leader>r :%s/<C-r><C-w>//g<Left><Left>
nnoremap <leader>u :GundoToggle<CR>
nnoremap <leader>- :Lex %:h<cr>
nnoremap <leader>gb :ls<CR>:b<Space>
nnoremap <leader>v :vert sfind
nnoremap <leader>gg :vimgrep // **/*.py \| clist \| call feedkeys(":cc ")<C-R>=setcmdpos(10)<CR><BS>

inoremap jh <Esc>

" " Copy to clipboard
vnoremap  <leader>y  "+y
nnoremap  <leader>Y  "+yg_
nnoremap  <leader>y  "+y
nnoremap  <leader>yy  "+yy   " Necessary?

" " Paste from clipboard
nnoremap <leader>p "+p
nnoremap <leader>P "+P
vnoremap <leader>p "+p
vnoremap <leader>P "+P

nmap <silent><Leader>f <Esc>:Pytest file<CR>
nmap <silent><Leader>c <Esc>:Pytest class<CR>
nmap <silent><Leader>m <Esc>:Pytest method<CR>
nmap <F8> :TagbarToggle<CR>

let g:netrw_winsize = 28                " absolute width of netrw window
let g:netrw_banner = 0                  " do not display info on the top of window
let g:netrw_liststyle = 3               " tree-view
let g:netrw_sort_sequence = '[\/]$,*'   " sort is affecting only: directories on the top, files below
let g:netrw_browse_split = 4            " use the previous window to open file

let g:gundo_prefer_python3 = 1

let g:session_autosave="yes"
let g:session_autoload="yes"

let g:better_whitespace_enabled=1
" let g:strip_whitespace_on_save=1

if has('nvim')
    set inccommand=nosplit
    tnoremap <Esc> <C-\><C-n>
endif

abbreviate breakpoint import pdb; pdb.set_trace()

source ~/.cocnvimrc
