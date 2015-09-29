#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Chatterbot.

Chatterbot is a program for the discipline of Formal Languages and
Automatons from the course of Computer Science at UFRGS.
"""

import random
import re

import chat_script_parser


def main(chat_script_path):
    """Run the main logic of the program."""
    try:
        initial, final, quit, pre, post, synon, key = \
            chat_script_parser.main(chat_script_path)
    except IOError:
        print("File not found. End of the program.")
    else:
        start_chat(initial, final, quit, pre, post, synon, key)


def is_quit(response, quit):
    """Check to see if the answer from the user is a quit one."""
    quits = []
    pattern = re.compile("\\b(quit:)\\W", re.I)
    quits = [pattern.sub("", word) for word in quit]
    combined = "(" + ")|(".join(quits) + ")"
    if re.search(combined, response):
        return True
    else:
        return False


def pre_proc(response, pre):
    """Do the pre processing of the response from the user."""
    pre_s = []
    pattern = re.compile("\\b(pre:)\\W", re.I)
    pre_s = [pattern.sub("", word) for word in pre]
    pre1, pre2 = zip(*(s.split(" ") for s in pre_s))
    dic_pre = dict(zip(pre1, pre2))
    pattern = re.compile(r'\b(' + '|'.join(dic_pre.keys()) + r')\b')
    return pattern.sub(lambda x: dic_pre[x.group()], response)


def post_proc(response, post):
    """Do the post processing of the response from the user."""
    post_s = []
    pattern = re.compile("\\b(post:)\\W", re.I)
    post_s = [pattern.sub("", word) for word in post]
    post1, post2 = zip(*(s.split(" ") for s in post_s))
    dic_post = dict(zip(post1, post2))
    pattern = re.compile(r'\b(' + '|'.join(dic_post.keys()) + r')\b')
    return pattern.sub(lambda x: dic_post[x.group()], response)


def sort_simple_message(list_of_messages):
    """Return a message from the list of messages."""
    random_index = random.randint(0, len(list_of_messages)-1)

    return list_of_messages[random_index]


def start_chat(initial, final, quit, pre, post, synon, key):
    """Chat loop."""
    # Prints initial message
    print("Eva:", sort_simple_message(initial))

    # Dialog loop
    while True:
        user_input = input("You: ")
        user_input = pre_proc(user_input)
        if is_quit(user_input, quit):
            print("Eva:", sort_simple_message(final))
            break
        # else:
            # search for the keys
            # post process
            # ??
