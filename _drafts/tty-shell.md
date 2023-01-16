# terminal, console, shell 和Vim 中的Meta

为了让我的mac + iTerm2 上的  `Vim` 支持 `Meta` 键真TM 复杂，放弃了!

## 术语

- **video terminal** 
- **virtual console** **TTY**
    - `/dev/tty<number>`
- **Pseudoterminals** **PTY**
    - `/dev/ptmx`
    - `/dev/pts/<pty_number>`

- **line editing**
- **line discipline**


## 一些工具

- `showkey -a`
- `stty -a`
- `tty`
- `who`

## Vim 相关

- [Vim 中正确使用 Alt映射](https://www.skywind.me/blog/archives/1846)
- [终端里正确设置 ALT 键和 BS 键](https://www.skywind.me/blog/archives/2021)
- [vim-rsi](https://github.com/tpope/vim-rsi)
- [vim term](https://vimdoc.sourceforge.net/htmldoc/term.html)

基本思路是先在终端模拟器上把 `Alt/Option` 键设置为 `ESC+`，
然后在 **Vim** 里把按下 `Alt/Option + {char}` 设置为 `\<ESC>{char}`，
再把 `<M-{char}>` 映射为对应的 `\<ESC>{char}`

```vim
set <M-a>=\<ESC>a
...
```

## 参考

- [linusakesson-tty](http://www.linusakesson.net/programming/tty/)
- [guide-terminal-shell-console](https://thevaluable.dev/guide-terminal-shell-console/)
- [Unix&Linux - What is the exact difference between a 'terminal', a 'shell', a 'tty' and a 'console'?](https://unix.stackexchange.com/questions/4126/what-is-the-exact-difference-between-a-terminal-a-shell-a-tty-and-a-con)
- [ANSI_escape_code](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [ANSI转义序列](https://zh.m.wikipedia.org/zh-hans/ANSI%E8%BD%AC%E4%B9%89%E5%BA%8F%E5%88%97)
- [GNU_Readline](https://en.wikipedia.org/wiki/GNU_Readline)

