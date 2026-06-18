#!/bin/python

import os

from term import *
from const import *

TANKSTRECK = "–"
SPACE_TAB = " " * 4

def main():
    text = ""
    sentence = ""
    in_quote = False
    dialog = False
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
            raw = raw[index+1:].lstrip()

        rendered += raw.lstrip() if did_wrap else raw
        write(ERASE_SCREEN + CUR_HOME + rendered)
        flush()

    def add_sentence():
        nonlocal text
        nonlocal sentence
        nonlocal dialog

        if 0 < len(sentence):
            if sentence[-1].isalnum():
                sentence += "."
                write(".")

        text += sentence + (" " if not dialog else "\n" + SPACE_TAB)
        sentence = ""
        dialog = False

        clear()

    def backspace():
        nonlocal sentence

        if 0 < len(sentence):
            is_tab = sentence.endswith(SPACE_TAB)
            n = len(SPACE_TAB) if is_tab else 1
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
                        if text == "":
                            prepend = SPACE_TAB
                        elif not text.endswith("\n" + SPACE_TAB):
                            prepend = "\n" + SPACE_TAB
                        else:
                            prepend = ""
                        sentence = prepend + TANKSTRECK + " "
                        write(ERASE_LINE + CUR_HOME + SPACE_TAB + TANKSTRECK + " ")
                        dialog = True
                    flush()
                    continue

        elif char == '"':
            char = "«" if in_quote else "»"
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

init()

try:
    result = main()
finally:
    restore()

os.system("clear")
print(result)

