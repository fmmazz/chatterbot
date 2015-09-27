#!/usr/bin/env python
# -*- coding: utf-8 -*-


def main(chat_script_path):
    try:
        read_content = read_file(chat_script_path)
    except IOError:
        print("File not found. End of the program.")
    else:
        parsed_content = parse_chat_content(read_content)
        print(parsed_content)

def read_file(chat_script_path):
    """Opens the file"""
    chat_script_file = open(chat_script_path)
    read_content = chat_script_file.read()
    chat_script_file.close()
    return read_content


def parse_chat_content(read_content):
    """Parses the read content, removing the format characters"""

    # Removes the encoding markup
    read_content = read_content.lstrip('\ufeff')

    # Removes whitespace and tabs from the strings
    # adding them to the result variable
    parsed_content = []
    for line in read_content.splitlines():
        line = line.strip(' \t')
        parsed_content.append(line)

    return parsed_content
