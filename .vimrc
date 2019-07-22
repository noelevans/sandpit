set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

Plugin 'tpope/vim-fugitive'
Plugin 'tpope/vim-surround'
Plugin 'tpope/vim-commentary'
Plugin 'itchyny/lightline.vim'
Plugin 'airblade/vim-gitgutter'
Plugin 'mhinz/vim-startify'
Plugin 'sjl/gundo.vim'

" Plugin 'w0rp/ale'
" Plugin 'neoclide/coc.nvim'

" After updating plugins, do:
"   :PluginUpdate

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Put your non-Plugin stuff after this line


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
set smartcase
set hlsearch
set incsearch 

" Don't redraw while executing macros (good performance config)
set lazyredraw 

" Show matching brackets under cursor
set showmatch 

" Tenths of second to blink when matching brackets
set mat=2

" No annoying sound on errors
set noerrorbells
set novisualbell
set t_vb=

set path+=**
set tags=tags
set showcmd
set undofile     " Persistent undo
set number
set relativenumber

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

" Ignore compiled files
set wildignore=*.o,*~,*.pyc
if has("win16") || has("win32")
    set wildignore+=.git\*,.hg\*,.svn\*
else
    set wildignore+=*/.git/*,*/.hg/*,*/.svn/*,*/.DS_Store
endif

hi CursorLine term=bold cterm=bold guibg=Grey40

" Enable syntax highlighting
syntax enable 

try
    colorscheme torte
catch
endtry

" Opens a new tab with the current buffer's path
" Super useful when editing files in the same directory
"map <leader>e :edit <c-r>=expand("%:p:h")<cr>/

" Switch CWD to the directory of the open buffer
"map <leader>cd :cd %:p:h<cr>:pwd<cr>

" Return to last edit position when opening files (You want this!)
"au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif

" Mark lines going past 80 characters
augroup vimrc_autocmds
  autocmd BufEnter * highlight OverLength ctermbg=darkgrey guibg=#111111
  autocmd BufEnter * match OverLength /\%80v.*/
augroup END

" Quickly open a markdown buffer for scribble
"map <leader>x :e ~/buffer.md<cr>

if has('unix')
    set clipboard=unnamedplus
endif

" Necessary for python-mode plugin to supress red 80 chars marker
hi ColorColumn ctermbg=8


noremap <Up> <Nop>
noremap <Down> <Nop>
noremap <Left> <Nop>
noremap <Right> <Nop>
noremap <PageUp> <Nop>
noremap <PageDown> <Nop>

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

" Toggle spell checking
map <leader>ss :setlocal spell!<cr>

nnoremap <leader>sop :source %<cr>
nnoremap <leader>h :nohl<cr>
nnoremap <leader>lint :ALEToggle<cr>
nnoremap <leader>r :%s/<C-r><C-w>//g<Left><Left>
nnoremap <leader>u :GundoToggle<CR>
nnoremap <leader>- :vert edit %:h<cr>


let g:netrw_winsize = -28               " absolute width of netrw window
let g:netrw_banner = 0                  " do not display info on the top of window
let g:netrw_liststyle = 3               " tree-view
let g:netrw_sort_sequence = '[\/]$,*'   " sort is affecting only: directories on the top, files below
let g:netrw_browse_split = 4            " use the previous window to open file

let g:gundo_prefer_python3 = 1

if has('nvim')
    set inccommand=nosplit
    tnoremap <Esc> <C-\><C-n>
endif
