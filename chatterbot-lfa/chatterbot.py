#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Chatterbot.

Chatterbot is a program for the discipline of Formal Languages and
Automatons from the course of Computer Science at UFRGS.
"""

import random
import re

import chat_script_parser


class ChatterBot:

    def __init__(self, initial, final, quit, pre, post, synon, key):
        self.initial = initial
        self.final = final
        self.quit = quit
        self.pre = pre
        self.post = post
        self.synon = synon
        self.key = key

    def start_chat(self):
        """Chat loop."""
        # Prints initial message
        self.print_simple_message(self.initial)
        # Dialog loop
        while True:
            user_input = self.get_user_input()
            if self.is_quit(user_input):
                self.print_simple_message(self.final)
                break
            else:
                matched_key = \
                    self.select_key_that_matches_user_input(user_input)
                response = self.decomp_to_regex(matched_key, user_input)


    def select_key_that_matches_user_input(self, user_input):
        """Match the user input with a key. Return the mached key"""
        # Match the user input with a key
        for index in range(len(self.key)):
            some_key = self.key[index]
            value_of_the_key = some_key[0]
            if value_of_the_key in user_input:
                break
        return self.key[index]

    def sort_simple_message(self, list_of_messages):
        """Return a message from the list of messages."""
        random_index = random.randint(0, len(list_of_messages)-1)
        return list_of_messages[random_index]

    def print_simple_message(self, message):
        print('Bot:', self.sort_simple_message(message))

    def get_user_input(self):
        user_input = input('You: ')
        user_input = user_input.lower()
        user_input = self.pre_proc(user_input)
        return user_input

    # Text processing methods that use regular expression
    def is_quit(self, response):
        """Check to see if the answer from the user is a quit one."""
        quits = []
        pattern = re.compile("\\b(quit:)\\W", re.I)
        quits = [pattern.sub("", word) for word in self.quit]
        combined = "(" + ")|(".join(quits) + ")"
        if re.search(combined, response):
            return True
        else:
            return False

    def pre_proc(self, response):
        """Do the pre processing of the response from the user."""
        pre_s = []
        pattern = re.compile("\\b(pre:)\\W", re.I)
        pre_s = [pattern.sub("", word) for word in self.pre]
        pre1, pre2 = zip(*(s.split(" ") for s in pre_s))
        dic_pre = dict(zip(pre1, pre2))
        pattern = re.compile(r'\b(' + '|'.join(dic_pre.keys()) + r')\b')
        return pattern.sub(lambda x: dic_pre[x.group()], response)

    def post_proc(self, response):
        """Do the post processing of the response from the user."""
        post_s = []
        pattern = re.compile("\\b(post:)\\W", re.I)
        post_s = [pattern.sub("", word) for word in self.post]
        post1, post2 = zip(*(s.split(" ") for s in post_s))
        dic_post = dict(zip(post1, post2))
        pattern = re.compile(r'\b(' + '|'.join(dic_post.keys()) + r')\b')
        return pattern.sub(lambda x: dic_post[x.group()], response)

    def decomp_to_regex(self, matched_key, response):
        key = matched_key[0]
        decomp = matched_key[1]
        if decomp == '*':
            result = re.search(r'()()', response)
        elif re.search(r'\*\s%s\s\*' % key, decomp):
            result = re.search(r'(.*)\s*%s\s*(.*)' % key, response)
        elif re.search(r'%s\s\*' % key, decomp):
            result = re.search(r'%s\s*(.*)' % key, response)
        else:
            result = re.search(r'(.*)\s*%s' % key, response)
        return result

    def sub_reasbm(reasbm, decomp):
        if re.search(r'\(1\)', reasbm):
            return re.sub(r'\(1\)', decomp.group(1), reasbm)
        else:
            return re.sub(r'\(2\)', decomp.group(2), reasbm)


def main(chat_script_path):
    """Run the main logic of the program."""
    try:
        initial, final, quit, pre, post, synon, key = \
            chat_script_parser.main(chat_script_path)
    except IOError:
        print("File not found. End of the program.")
    else:
        AChatterBot = ChatterBot(initial, final, quit, pre, post, synon, key)
        AChatterBot.start_chat()
