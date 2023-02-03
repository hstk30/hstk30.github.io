---
layout:     post
title:      "PracticalVim 笔记"
date:       2022-05-19
author:     "hstk30"
header-img: "img/tame.jpg"
description: "熟能通其窍，精能尽其妙。"
tags:
    - Vim
    - 读书笔记
---


# Practical Vim note

## core

- Act, Repeat, Reverse
- Dot Formula: One Keystroke to Move, One Keystroke to Execute


### Combo

- line/word action: `{action} {move}.{move}.{move}.`
- line search action: `f{char} ;.;.;.`
- search action: `/pattern {action} n.n.n.`, `* {action} n.n.n.`
- macros: `q{reg} {actions} q @{reg} {move} @@ {move} @@`
- normal: `:[range]normal {cmd}`

## mode

### Insert Mode

#### Digraph

- `:digraphs` : Display the digraphs available

Some useful **Digraph** :

- `CTRL+K AN` : **∧** , logic and
- `CTRL+K OR` : **∨** , logic or
- `CTRL+K NO` : **¬** , logic not
- `CTRL+K (-` : **∈** 
- `CTRL+K ->` : **→**
- `CTRL+K OK` : **✓**
- `CTRL+K XX` : **✗**


### Command-Line Mode

#### Address

- `.`: the current line.
- `$`: the last line in the file.
- `%`: the entire file
- `'m`: mark line
- `/pattern/`: `:/<html>/,/<\/html>/p`
- `{address}+n`: set offset `.,.+3p`

#### Range

```
:{start_addresss},{end_address}
```

#### Ex commands

- `:[range]delete [reg]` : delete the `range` lines into the register
- `:[range]yank [reg]`
- `:[range]put [reg]`
- `:[range]copy {address}` : copy the `range` lines below the `{address}`
- `:[range]move {address}`
- `:[range]normal {commands}`: execute `{commands}` on the `range` lines
- `!{cmd}` : execute `{cmd}` with the shell
- `read !{cmd}` : execute `{cmd}`, insert the output to buffer
- `[range]write !{cmd}` : like in shell `> cmd < content of [range]`
- `[range]!{filter}` : Filter the specified `range` through external program `{filter}`
- `[range]sort` : sort `range` lines

#### tips

- `:'<,'>normal 0i# `: 选中区域，简单添加 `Python` 注释
- `:'<,'>normal i//`: 选中区域，添加 `C99` 注释
- `<C-f>`: Switch from Command-Line mode to the command-line window

## motions

### real line and display line

- `gj`: down one **display** line
- `gk`: up one **display** line

### diff *Words* from *WORDS*

Like `e.g. We` have four *Words* , but a *WORDS* , which means that 
need keystrokes `www` to move from `e` to `W` , but `W` to reach directly.

### find by char

`f{char}` and `F{char}` to location char, 
`t{char}` and `T{char}` to `d{motion}` or `c{motion}`.

Like: `dt.` delete till char `.` , exclude char `.` .


### text-objects

#### Build-in text-objects

- `aw` `iw`: a/inner word
- `aW` `iW`: a/inner **WORD**
- `as` `is`: a/inner sentence
- `ap` `is`: a/inner paragraph
- `a]` `i]`: a/inner **[]**
- `a)` `i)`: a/inner **()**
- `a>` `i>`: a/inner **<>**
- `at` `it`: a/inner **<xml></xml>**
- `a}` `i}`: a/inner **Block**
- `a\"` `i\"`: a/inner **\"**
- `a\'` `i\'`: a/inner **\'**

#### other useful text-object

- `aa` `ia`: a/inner argument provided by [argtextobj.vim](https://www.vim.org/scripts/script.php?script_id=2699)
- `ai` `ii` `aI` `iI`: a/inner same indentation level provided by [vim-indent-object](https://github.com/michaeljsmith/vim-indent-object)
- `ae` `ie`: a/inner entire content of a buffer provided by [vim-textobj-entire](https://github.com/kana/vim-textobj-entire)

... 


### marks

- **m{a-zA-Z}**: set mark, lowercase marks local, uppercase marks global.
- **\`{mark}** : go to mark position.
- **\'{mark}** : go to mark line.

### automatic marks

- **\`\`** : last jump within current file
- **\`\.** : last change
- **\`^** : last insert
- **\`[** :  start of last change or yank
- **\`]** :  end of last change or yank
- **\`<** :  start of last visual selection
- **\`>** :  end of last visual selection

Visual model + `:`: `:'<,'>` select the visual range.

### tips

- Mark the position by `mm` before search `/pattern`, 
    when done all matched, return the marked position by **\`m**
- Search by `vimgrep` or `ack` in project files, mark the position by `mM` first, 
    return the marked position by **\`M**


## files

[LeaderF](https://github.com/Yggdroot/LeaderF) is super useful.

#### argument-list, buffer-list

- `:argdo {cmd}`, like `:argdo normal @{reg}`
- `:bufdo {cmd}`

## registers

> Vim’s registers are no more than containers for strings of text.


### special registers

- `""`: unnamed register
- `"0`: yank register
- `"1-"9`: numbered registers
- `"+`: system clipboard
- `"_`: black hole 
- `"=`: expression register
- `=%`: name of current file
- `"#`: name of the alternate file
- `".`: last inserted text
- `":`: last Ex command
- `"/`: last search pattern
- `"a-"z`: named registers

#### Combo

1. `[reg] {operator} {motion}`, like `"ayiw -> "ap`
2. Insert/EX mode: `<C-r> {reg}`, like `<C-r> 0`, `:%s//<C-r>0/g`

#### CTRL-R CTRL-{X}

Insert the object under the cursor:

- `CTRL-R CTRL-F`: filename
- `CTRL-R CTRL-W`: word
- `CTRL-R CTRL-A`: WORD
- `CTRL-R CTRL-L`: line text

### macros

#### tips 

- **Ex Command** can also be record
- use `q{upper char}` to append extra cmd to the exist `cmd`

#### Combo

1. `q{reg} {change cmd} {repeatable motion}`, `100@{reg}`: ensure the record action 
    start/end with a **repeatable motion** like `n/f{x}/w/...`
2. repeat **Dot Operator**: `qq {motion}. q` + `{num}@q`, like `qq ;. q 22@q`


## patterns

### specify a broad pattern

- `\<`: beginning of a word
- `\>`: end of a word
- `\zs`: set the start of the match
- `\ze`: set the end of the match

Like: `/\v[\zs\a*\ze\]` search all normal word in `[]`, but just match the word.


### search-offset

`/pattern/e<CR>` let the cursor at the end of the search match.

> When we leave the search field blank, Vim reuses the pattern from the previous search.

So `//e<CR>` incrementally search.


### substitute

```
:[range]s[ubstitute]/[pattern]/{string}/[flags]
```

#### s_flags

- `&`: use the previous substitute's flags
- `g`: *global* line
- `c`: confirm
- `n`: Report the number of matches, do not actually substitute


#### tips

1. `g&` == `:%s//~/&`: repeat last substitute
2. `:'<,'>&&`: select range in visual mode, then replay the substitute by `:&&`
3. `:%&&` == `g&`

### global

```
:[range] global[!] /{pattern}/ [cmd]
```

#### tips

- `:g/useless/norm gu$`: combine a normal mode command with the global command, powerful!
- `:g/TODO/copy$`: copy to the end of file for all the line which match the `TODO`.


## Tools

### ctags

Now use [universal ctags](https://github.com/universal-ctags/ctags) instead of `exuberant-ctags`

- `<C-]>` : jump to the first tag 
- `g<C-]>` : prompt user to select from multiple matches
- `:tprev`
- `:tnext`


Use [vim-gutentags](https://github.com/ludovicchabant/vim-gutentags) to generate *ctags* automatically.


### quickfix

- `:copen` : open the quickfix window
- `:cclose` : close the quickfix window
- `:cnext` : jump to next item
- `:cprev` : jump to previous item
- `:cfirst` : jump to first item
- `:cnext` : jump to next item
- `:cnfile` : jump to first item in next file
- `:cpfile` : jump to first item in previous file
- `:cc N` : jump to nth item

* `:colder`: previous quickfix list
* `:cnewer`: next quickfix list

### autocompletion

- `<C-n>` `<C-p>` : generic keywords
- `<C-x><C-l>` : whole line completion
- `<C-x><C-f>` : filename completion
- `<C-x><C-n>` : from current buffer 
- `<C-x><C-i>` : from include files
- `<C-x><C-]>` : from `tags` file
- `<C-x><C-k>` : from `Dictionary` file
- `<C-x><C-o>` : Omni-completion

### spell checker

- `set spell` : enable the spell checker
- `[s` : previous misspelled word
- `]s` : next misspelled word
- `z=` : suggest corrections
- `zg` : add the word to spell dictionary
- `zw` : remove the word from spell dictionary
- `zug` : Revert `zg` or `zw` command

* Spell file default path: `~/.vim/spell/`
* Set Chinese spell dictionary: `set spelllang=en_us,cjk`

+ `<C-x>s` : spell correct automatically in the insert mode

## misc

### `g`字诀

### `z`字诀

###  `[`字诀

大多`[` 相关的命令和前进/后退相关，因此有

[vim-unimpaired](https://github.com/tpope/vim-unimpaired)

这个对`[` 的扩充。


文本对象：

1. **sentence** 
2. **paragraph** : 空行分隔为一个 **paragraph**
3. **section** : `{}` 包围为一个 **section** ，但要求`{` 在第一列，因此`C` 代码的函数最好写成

    ```
    int func()
    {

    }
    ```
    的格式

作用区域： **sentence** `<=` **paragraph** `<=` **section**


- `)` : forword sentence
- `(` : backword sentence
- `}` : forword paragraph
- `{` : backword paragraph
- `]]` : forword section to `{`
- `[[` : backword section to `{`
- `][` : forword section to `}`
- `[]` : backword section to `}`


## end

Practice -> Pain -> Patient -> Practice ... -> Perfect

`:x`

## More 

- [VIM 中文参考手册](https://vimcdoc.sourceforge.net/doc/)
- [VIM docs](https://vimdoc.sourceforge.net/)
- [Seven habits of effective text editing](https://www.moolenaar.net/habits.html)
- [vimcasts.org](http://vimcasts.org/episodes/)
