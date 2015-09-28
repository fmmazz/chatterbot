#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Chatterbot.

Chatterbot is a program for the discipline of Formal Languages and
Automatons from the course of Computer Science at UFRGS.
"""


import chat_script_parser

def main(chat_script_path):
    """Run the main logic of the program."""
    try:
        chat_script_parser.main(chat_script_path)
    except IOError:
        print("File not found. End of the program.")
    # else:
