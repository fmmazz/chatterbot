#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main(chat_script_path):
    try:
        chat_script_file = open(chat_script_path)
        read_content = chat_script_file.read()
        chat_script_file.close()
    except IOError:
        print("File not found.")
