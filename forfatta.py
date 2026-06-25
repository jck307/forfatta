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
OPENING_QUOTE = "»"
CLOSING_QUOTE = "«"

def main():
    text = ""
    sentence = ""
    cursor = 0
    in_quote = False

    def add_sentence():
        nonlocal text, sentence, cursor

        if sentence == "":
            text += "\n"

        elif not sentence.isspace():
            sentence = sentence.rstrip()
            text += sentence + (". " if sentence[-1].isalnum() else " ")
            sentence = ""
            cursor = 0

    def backspace():
        nonlocal sentence, cursor, in_quote

        n = len(SPACE_TAB) if sentence[cursor-len(SPACE_TAB):cursor] == SPACE_TAB else 1
        if n == 1:
            if sentence[cursor-1] == OPENING_QUOTE:
                in_quote = False
            elif sentence[cursor-1] == CLOSING_QUOTE:
                in_quote = True

        sentence = sentence[:cursor-n] + sentence[cursor:]
        cursor = max(0, cursor - n)

    def render(text):
        raw = text[:cursor] + CUR_SAVE + text[cursor:]
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
        rendered = rendered.replace("\n", CUR_DOWN_ONE + CUR_COL_HOME)
        write(ERASE_SCREEN + CUR_HOME + rendered + CUR_RESTORE)
        flush()

    while True:
        term_cols, _ = os.get_terminal_size()
        render(sentence)
        char = read()

        if char in [ESCAPE, CTRL_C]:
            add_sentence()
            break

        elif char == CTRL_P:
            write(CUR_HIDE)
            render(text)
            while read() != CTRL_P:
                pass
            write(CUR_SHOW)
            continue

        elif char == BACKSPACE:
            backspace()
            continue

        elif char == CTRL_BACKSPACE:
            while cursor != 0 and sentence[cursor-1] == " ":
                backspace()
            while cursor != 0 and sentence[cursor-1] != " ":
                backspace()
            continue

        elif char == RETURN:
            add_sentence()
            continue

        elif char == ARROW_LEFT:
            cursor = max(0, cursor - 1)
            continue

        elif char == ARROW_RIGHT:
            cursor = min(len(sentence), cursor + 1)
            continue

        elif char == CTRL_ARROW_LEFT:
            try:
                cursor = sentence.rindex(" ", 0, cursor)
            except ValueError:
                cursor = 0
            continue

        elif char == CTRL_ARROW_RIGHT:
            try:
                cursor = sentence.index(" ", cursor+1)
            except ValueError:
                cursor = len(sentence)
            continue

        elif char in HOME:
            cursor = 0
            continue

        elif char in END:
            cursor = len(sentence)
            continue

        elif char == "\t":
            char = SPACE_TAB
        
        elif char == '"':
            char = CLOSING_QUOTE if in_quote else OPENING_QUOTE
            in_quote = not in_quote

        elif char == "-":
            if cursor != 0 and sentence[cursor-1] == "-":
                sentence = sentence[:cursor-1] + TANKSTRECK \
                    + (" " if cursor == 1 else "") + sentence[cursor:]
                if cursor == 1:
                    cursor += 1
                    if text == "" or text.endswith("\n"):
                        sentence = SPACE_TAB + sentence
                        cursor += len(SPACE_TAB)
                continue

        alnum_found = False
        for prev_char in sentence:
            if prev_char.isalnum():
                alnum_found = True
                break

        if not alnum_found:
            char = char[0].upper() + char[1:]

        sentence = sentence[:cursor] + char + sentence[cursor:]
        cursor += len(char)

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

