# forfatta

![banner](/banner.png?raw=true)

A little terminal utility I made for creative writing.

The interesting part about it is that once you enter a sentence (by pressing enter), it disappears and you are unable to go back and edit it – as if you were writing with ink on paper! Does that sound retarded? Well, it is to some extent, but it might also enhance creativity since you are forced to write in a different way, as well as productivity since you literally can not obsess over stuff like spelling, grammar etc. Once you are done, pressing escape exits the program, spits out the text and saves it to a file.

## Usage

```
usage: forfatta.py [-h] [--no-save] [--no-timestamp] [filename]

positional arguments:
  filename

options:
  -h, --help      show this help message and exit
  --no-save
  --no-timestamp
```

## Binds

- Navigation: left, right, ctrl+left, ctrl+right, home, end
- Alternatives: alt+h, alt+l, alt+ctrl+h, alt+ctrl+l, alt+0, alt+'+'
- See written text (toggle): ctrl+p
- Deleting: backspace, delete, ctrl+backspace, ctrl+delete
- Delete whole row: ctrl+y
- Save and quit: escape, ctrl+c

## Features

- Automatic uppercase in the beginning of sentences
- Automatic insertion of space after sentences
- Automatic insertion of `.` if punctuation is omitted
- `"` is replaced with `»` and `«` (for opening and closing respectively)
- Two hyphens (--) are replaced with a dash (–)
- Files are appended to, not overwritten
- `output.txt` is used unless a filename is given or `--no-save` is used
