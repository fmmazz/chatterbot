#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Chatterbot.

Chatterbot is a program for the discipline of Formal Languages and
Automatons from the course of Computer Science at UFRGS.
"""

import random
import re


class ChatterBot:

    def __init__(self, initial, final, quit, pre, post, synon, key):
        """Set the chatterbot attributes."""
        self.bot_name = "Bot"
        self.user_name = "You"
        self.initial = initial
        self.final = final
        self.quit = quit
        self.pre = pre
        self.post = post
        self.synon = synon
        self.key = key
        self.keys_weight = self.define_weight_to_key()

    def start_chat(self):
        """Chat loop."""
        # Prints initial message
        self.print_simple_message(self.initial[0])
        # Dialog loop
        while True:
            user_input = self.get_user_input()
            user_input = self.pre_proc(user_input)
            if self.is_quit(user_input):
                final_phr = self.sort_simple_message(self.final)
                self.print_simple_message(final_phr)
                break
            else:
                matched_key = self.select_key_that_matches_user_input(
                    user_input)
                response = self.decomp_to_regex(matched_key,
                                                user_input)
                reasbm_phr = self.pick_a_reasmb_phrase(matched_key[2])
                final_phr = self.sub_reasbm(reasbm_phr, response)
                self.print_simple_message(final_phr)

    def define_weight_to_key(self):
        keys_weight = {}
        for index in range(len(self.key)):
            some_key = self.key[index]
            value_of_the_key = some_key[0]
            phrase = re.search(r'(\w*)\s*(\d*)', value_of_the_key)
            if not phrase.group(2):
                keys_weight[phrase.group(1)] = 0
            else:
                value = int(phrase.group(2))
                keys_weight[phrase.group(1)] = value
            self.key[index][0] = phrase.group(1)
        return keys_weight

    def select_key_that_matches_user_input(self, user_input):
        """Match the user input with a key. Return the mached key."""
        keys_matched = []
        words_of_user_input = self.string_to_list_of_words(user_input)
        # Match the user input with a key
        for index in range(len(words_of_user_input)):
            if words_of_user_input[index] in self.keys_weight:
                keys_matched.append(words_of_user_input[index])
        keys_matched = sorted(
            keys_matched, key=lambda x: self.keys_weight[x], reverse=True)

        if not keys_matched:
            return (self.key[len(self.key) - 1])
        else:
            index = 0
            for index in range(len(self.key)):
                k_word = re.search(r'(\w*)', self.key[index][0])
                if keys_matched[0] == k_word.group(1):
                    return self.key[index]

    def string_to_list_of_words(self, user_string):
        """Split the user input in words, save in list."""
        list_of_words = []
        for word in user_string.split():
            word = word.strip(".,;?")
            list_of_words.append(word)
        return list_of_words

    def pick_a_reasmb_phrase(self, list_of_reasmb_phrases):
        """Return a message from the list of messages."""
        # Search for a random reasmb phrase wich is not used yet
        counter = 0
        lenght_of_the_list = len(list_of_reasmb_phrases)
        while counter < lenght_of_the_list:
            sorted_reasmb_phrase = list_of_reasmb_phrases[counter]
            if sorted_reasmb_phrase[1] is False:
                sorted_reasmb_phrase[1] = True
                return sorted_reasmb_phrase[0]
            else:
                counter += 1
        # If all phrases ared used, mark all them as not used
        list_of_reasmb_phrases = self.mark_reasmb_as_not_used(
            list_of_reasmb_phrases)
        # Returns the first one
        list_of_reasmb_phrases[0][1] = True
        return list_of_reasmb_phrases[0][0]

    def mark_reasmb_as_not_used(self, list_of_reasmb_phrases):
        for reasbm_phrase in list_of_reasmb_phrases:
            reasbm_phrase[1] = False
        return list_of_reasmb_phrases

    def sort_simple_message(self, list_of_messages):
        """Return a message from the list of messages."""
        random_index = random.randint(0, len(list_of_messages) - 1)
        return list_of_messages[random_index]

    def print_simple_message(self, message):
        """Print the passed message and the bot name in front of it."""
        print(self.bot_name + ':', message)

    def get_user_input(self):
        """Ask for the user input, showing the defined name for it."""
        user_input = input(self.user_name + ': ')
        return user_input

    # Text processing methods that use regular expression
    def is_quit(self, response):
        """Check to see if the answer from the user is a quit one."""
        quits = []
        pattern = re.compile("\\b(quit:)\\W", re.I)
        quits = [pattern.sub("", word) for word in self.quit]
        combined = "(" + ")|(".join(quits) + ")"
        if re.search(combined, response, re.IGNORECASE):
            return True
        else:
            return False

    def pre_proc(self, response):
        """
        Do the pre processing of the response from the user. Binds together
        relate words in pre list. Separate in two lists (no graphic mark and
        with graphic mark. Binds together in dict no graphic: with graphic.
        Finds word and replace by your content in dict.
        """
        pre_s = []
        pattern = re.compile("\\b(pre:)\\W", re.I)
        pre_s = [pattern.sub("", word) for word in self.pre]
        pre1, pre2 = zip(*(s.split(" ") for s in pre_s))
        dic_pre = dict(zip(pre1, pre2))
        pattern = re.compile(r'\b(' + '|'.join(dic_pre.keys()) + r')\b')
        return pattern.sub(lambda x: dic_pre[x.group()], response)

    def post_proc(self, response):
        """
        Do the post processing of the response from the user. Binds together
        relate words in post list. Separate in two lists and bind together in
        dict, like
            dict => key: word to be replaced
        Finds word and replace by your content in dict.
        """
        post_s = []
        pattern = re.compile("\\b(post:)\\W", re.I)
        post_s = [pattern.sub("", word) for word in self.post]
        post1, post2 = zip(*(s.split(" ") for s in post_s))
        dic_post = dict(zip(post1, post2))
        pattern = re.compile(r'\b(' + '|'.join(dic_post.keys()) + r')\b')
        return pattern.sub(lambda x: dic_post[x.group()], response)

    def decomp_to_regex(self, matched_key, response):
        """
        Transform the decomp item from the key in regex and separate in groups.
        """
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

    def sub_reasbm(self, reasbm, decomp):
        """
        Apply the post_proc in user answer and replace user content in reasbm
        if needed.
        """
        if re.search(r'\(1\)', reasbm):
            phrase = self.post_proc(decomp.group(1))
            return re.sub(r'\(1\)', phrase, reasbm)
        elif re.search(r'\(2\)', reasbm):
            phrase = self.post_proc(decomp.group(2))
            return re.sub(r'\(2\)', phrase, reasbm)
        else:
            return reasbm
