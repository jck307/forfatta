#!/bin/python

import os
import sys
import datetime
import argparse

csfp = os.path.abspath(os.path.dirname(__file__))
if csfp not in sys.path:
    sys.path.insert(0, csfp)

from term import *
from const import *

TANKSTRECK = "–"
SPACE_TAB = " " * 4
CLOSING_QUOTE = "«"
OPENING_QUOTE = "»"

def main():
    text = ""
    sentence = ""
    in_quote = False
    clear_next = False

    def clear():
        write(ERASE_SCREEN + CUR_HOME)
        flush()

    def render_sentence():
        raw = sentence
        rendered = ""

        did_wrap = term_cols-1 < len(raw)

        while term_cols-1 < len(raw):
            if raw[term_cols-1].isspace():
                index = term_cols
            else:
                try:
                    index = raw.rindex(" ", 0, term_cols-1)
                except ValueError:
                    break

            rendered += raw[:index].rstrip() + CUR_DOWN_ONE + CUR_COL_HOME
            raw = raw[index:].lstrip()

        rendered += raw.lstrip() if did_wrap else raw
        write(ERASE_SCREEN + CUR_HOME + rendered)
        flush()

    def add_sentence():
        nonlocal text
        nonlocal sentence

        if 0 < len(sentence):
            if sentence[-1].isalnum():
                sentence += "."
                write(".")

        text += sentence + " "
        sentence = ""

        clear()

    def backspace():
        nonlocal sentence
        nonlocal in_quote

        if 0 < len(sentence):
            is_tab = sentence.endswith(SPACE_TAB)
            n = len(SPACE_TAB) if is_tab else 1
            if n == 1:
                if sentence[-1] == OPENING_QUOTE:
                    in_quote = False
                elif sentence[-1] == CLOSING_QUOTE:
                    in_quote = True
            sentence = sentence[:-n]
            render_sentence()

    while True:
        char = read()

        if clear_next:
            clear_next = False
            write(CUR_SHOW)
            clear()

        term_cols, _ = os.get_terminal_size()

        if char in [ESCAPE, CTRL_C]:
            add_sentence()
            break

        elif char == BACKSPACE:
            backspace()
            flush()
            continue

        elif char == CTRL_BACKSPACE:
            while 0 < len(sentence) and sentence[-1] == " ":
                backspace()
            while 0 < len(sentence) and sentence[-1] != " ":
                backspace()
            flush()
            continue

        elif char == RETURN:
            if sentence == "":
                ASTERISM = f"* *{CUR_DOWN_ONE}{CUR_COL_HOME} *" + CUR_HIDE
                if text.endswith("\n" + SPACE_TAB):
                    text = text[:-1] + "\n"
                    write(ASTERISM)
                    flush()
                    clear_next = True
                else:
                    if not text.endswith("\n"):
                        text += "\n" + SPACE_TAB
                        write("*" + CUR_HIDE)
                    else:
                        write(ASTERISM)
                    flush()
                    clear_next = True
            else:
                add_sentence()
            continue

        elif char == "\t":
            if not sentence.endswith(" "):
                sentence += SPACE_TAB
                write(SPACE_TAB)
                flush()
            continue

        elif char == "-":
            if 0 < len(sentence):
                if sentence[-1] == "-":
                    if len(sentence) != 1:
                        sentence = sentence[:-1] + TANKSTRECK
                        write(CUR_LEFT_ONE + TANKSTRECK)
                    else:
                        if 0 < len(text):
                            text += "\n"
                        sentence = SPACE_TAB + TANKSTRECK + " "
                        write(ERASE_LINE + CUR_HOME + SPACE_TAB + TANKSTRECK + " ")
                    flush()
                    continue

        elif char == '"':
            char = CLOSING_QUOTE if in_quote else OPENING_QUOTE
            in_quote = not in_quote

        elif char == " ":
            if sentence.endswith(" "):
                continue

        alnum_found = False
        for prev_char in sentence:
            if prev_char.isalnum():
                alnum_found = True
                break

        if not alnum_found:
            char = char.upper()

        sentence += char
        render_sentence()

    return text.replace(SPACE_TAB, "\t").rstrip()

parser = argparse.ArgumentParser(color=False)
parser.add_argument("filename", default="output.txt", nargs="?")
parser.add_argument("--no-save", action="store_true")
parser.add_argument("--no-timestamp", action="store_true")
args = parser.parse_args()

init()

try:
    result = main()
finally:
    restore()

os.system("clear")

if result.isspace() or result == "":
    exit()

print(result)

if not args.no_save:
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M]\n") if not args.no_timestamp else ""

    with open(args.filename, "a") as file:
        file.write(timestamp + result + "\n")

    print("saved to", args.filename)

