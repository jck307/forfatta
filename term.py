import os
import sys
import tty
import termios

from const import *

stdin = None
stdout = None

fd = None
old_settings = None

def _init():
    global stdin, stdout, fd, old_settings

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(sys.stdin)

    stdin = sys.stdin.buffer
    stdout = sys.stdout

def _restore():
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def close_stdin():
    stdin.close()

def init():
    _init()
    write(RESET + ERASE_SCREEN + CUR_HOME)
    flush()

def restore():
    write(RESET + ERASE_SCREEN + CUR_HOME + CUR_SHOW)
    _restore()
    flush()

def read():
    return stdin.read1().decode()

def write(string):
    stdout.write(string)

def flush():
    stdout.flush()

def get_max_yx():
    x, y = os.get_terminal_size()
    return y, x

