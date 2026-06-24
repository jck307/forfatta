# forfatta

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

## Features

- Automatic uppercase in the beginning of sentences
- Automatic insertion of space after sentences
- Automatic insertion of `.` if punctuation is not given
- Ctrl-binds (backspace, arrows)
- Ctrl-P (a toggle) lets you inspect written text
- `"` is replaced with `»` and `«` (for opening and closing respectively)
- `--` is replaced with `–`
- Files are appended to
- `output.txt` is saved to unless a filename is given or `--no-save` is used
