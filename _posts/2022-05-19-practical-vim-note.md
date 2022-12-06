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


## mode

### command-line mode

#### range

```
:{start},{end}
```

- `.`: the current line.
- `$`: the last line in the file.
- `%`: the entire file
- `'m`: mark line

## motions

### real line and display line

- `gj`: down one **display** line
- `gk`: up one **display** line

### diff *Words* from *WORDS*

like `e.g. We` have four *Words* , but a *WRODS* , which means that 
need keystrokes `www` to move from `e` to `W` , but `W` to reach directly.

### find by char

`f{char}` and `F{char}` to location char, 
`t{char}` and `T{char}` to `d{motion}` or `c{motion}`.

like: `dt.` delele till char `.` , exclude char `.` .


### text objects

So important, and use it so frequent that omniscient.


### marks

- **m{a-zA-Z}**: set mark, lowercase marks local, uppercase marks global.
- **\`{mark}** : go to mark position.
- **\'{mark}** : go to mark line.

### automatic marks

- **\`\`** : last jump within current file
- **\`\.** : last change
- **\`\^** : last insert
- **\`\^** : last insert

other like **\`[** , **\`]** , **\`<** , **\`>** use less.


## files

[LeaderF](https://github.com/Yggdroot/LeaderF) is super useful.


## registers

### specical registers

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

### macros

pass

## patterns

### specify a broad pattern

- `\zs`: set the start of the match
- `\ze`: set the end of the match

like: `/\v[\zs\a*\ze\]` search all normal word in `[]`, but just match the word.


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



