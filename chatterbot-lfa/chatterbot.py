#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Chatterbot.

Chatterbot is a program for the discipline of Formal Languages and
Automatons from the course of Computer Science at UFRGS.
"""

import random
import re


class ChatterBot:
    """The class for the chatterbot."""

    def __init__(self, initial, final, quit, pre, post, synon, key):
        """Set the chatterbot attributes."""
        self.bot_name = "Eu"
        self.user_name = "Você"
        self.initial = initial
        self.final = final
        self.quit = quit
        self.pre = pre
        self.post = post
        self.synon = synon
        self.key = key
        self.dict_of_synon = self.synon_to_dict()

    def start_chat(self):
        """Chat loop."""
        # Prints initial message
        self.print_simple_message(self.initial[0])
        self.key = sorted(self.key, key=lambda x: x[1], reverse=True)
        # Dialog loop
        while True:
            user_input = self.get_user_input()
            user_input = self.pre_proc(user_input)
            if self.is_quit(user_input):
                final_phr = self.sort_simple_message(self.final)
                self.print_simple_message(final_phr)
                break
            else:
                reasbm_list, decomp_user_input = self.search_keys(user_input)
                reasbm_phr = self.pick_a_reasmb_phrase(reasbm_list)
                final_phr = self.sub_reasbm(reasbm_phr, decomp_user_input)
                self.print_simple_message(final_phr)

    def get_user_input(self):
        """Ask for the user input, showing the defined name for it."""
        user_input = input(self.user_name + ': ')
        user_input = user_input.lower()
        return user_input

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
        """Change all the reasmb values to false."""
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

    def synon_to_dict(self):
        """Put synon to a dict with key as the word found in decomp."""
        syn_dict = {}
        list_of_syn = []
        for i in range(len(self.key)):
            for j in range(0, len(self.key[i][2]), 2):
                if re.search(r'\*\s\@\w+\s\*', self.key[i][2][j]):
                    word_syn = re.search(
                        r'\*\s\@(\w+)\s\*', self.key[i][2][j]).group(1)
                elif re.search(r'\@\w+\s\*', self.key[i][2][j]):
                    word_syn = re.search(
                        r'\@(\w+)\s\*', self.key[i][2][j]).group(1)
                elif re.search(r'\*\s\@\w+', self.key[i][2][j]):
                    word_syn = re.search(
                        r'\*\s\@(\w+)', self.key[i][2][j]).group(1)
                else:
                    break

                for w in range(len(self.synon)):
                    if word_syn in self.synon[w]:
                        list_of_syn = self.synon[w].split(' ')
                        syn_dict[word_syn] = list_of_syn
        return syn_dict

    def pre_proc(self, response):
        """
        Do the pre processing of the response from the user.

        Binds together relate words in pre list. Separate in two lists
        (no graphic mark and with graphic mark. Binds together in dict no
        graphic: with graphic. Finds word and replace by your content in dict.
        """
        pre_s = []
        pattern = re.compile("\\b(pre:)\\W", re.I)
        pre_s = [pattern.sub("", word) for word in self.pre]
        pre1, pre2 = zip(*(s.split(" ") for s in pre_s))
        dic_pre = dict(zip(pre1, pre2))
        pattern = re.compile(r'\b(' + '|'.join(dic_pre.keys()) + r')\b')
        return pattern.sub(lambda x: dic_pre[x.group()], response)

    def search_keys(self, user_input):
        for i in range(len(self.key)):
            for j in range(0, len(self.key[i][2]), 2):
                if re.search(r'.*\@.*', self.key[i][2][j]):
                    if re.search(r'\*\s\@\w+\s\*', self.key[i][2][j]):
                        syn_to_search = re.search(
                            r'\*\s\@(\w+)\s\*', self.key[i][2][j]).group(1)
                    elif re.search(r'\@\w+\s\*', self.key[i][2][j]):
                        syn_to_search = re.search(
                            r'\@(\w+)\s\*', self.key[i][2][j]).group(1)
                    elif re.search(r'\*\s\@\w+', self.key[i][2][j]):
                        syn_to_search = re.search(
                            r'\*\s\@(\w+)', self.key[i][2][j]).group(1)
                    syn_to_compare = self.dict_of_synon[syn_to_search]
                    for w in range(len(self.dict_of_synon[syn_to_search])):
                        if re.search(r'\b%s\b' % syn_to_compare[w], user_input):
                            patt = syn_to_compare[w]
                            result = re.search(
                                r'(.*)\s*(%s)\s*(.*)' % patt, user_input)
                            return self.key[i][2][j + 1], result
                if self.key[i][2][j] == '*':
                    patt = self.key[i][0]
                    if self.key[i][0] == '*' or re.search(r'\b%s\b' % patt, user_input):
                        result = re.search(r'()()', user_input)
                        return self.key[i][2][j + 1], result
                elif re.search(r'\*\s.*\s\*', self.key[i][2][j]):
                    patt = re.search(
                        r'\*\s(.*)\s\*', self.key[i][2][j]).group(1)
                    if re.search(r'\b%s\b' % patt, user_input):
                        result = re.search(r'(.*)\s*%s\s*(.*)' %
                                           patt, user_input)
                        return self.key[i][2][j + 1], result
                elif re.search(r'.*\s\*', self.key[i][2][j]):
                    patt = re.search(r'(.*)\s\*', self.key[i][2][j]).group(1)
                    if re.search(r'\b%s\b' % patt, user_input):
                        result = re.search(r'%s\s*(.*)' % patt, user_input)
                        return self.key[i][2][j + 1], result
                else:
                    patt = re.search(r'\*\s(.*)', self.key[i][2][j]).group(1)
                    if re.search(r'\b%s\b' % patt, user_input):
                        result = re.search(r'(.*)\s*%s' % patt, user_input)
                        return self.key[i][2][j + 1], result

    def post_proc(self, response):
        """
        Do the post processing of the response from the user.

        Binds together relate words in post list. Separate in two lists and
        bind together in dict, like
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

    def sub_reasbm(self, reasbm, decomp):
        """
        Mount the answer.

        Apply the post_proc in user answer and replace user content in reasbm,
        if needed.
        """
        if re.search(r'\(1\)', reasbm):
            phrase = self.post_proc(decomp.group(1))
            return re.sub(r'\(1\)', phrase, reasbm)
        elif re.search(r'\(2\)', reasbm):
            phrase = self.post_proc(decomp.group(2))
            return re.sub(r'\(2\)', phrase, reasbm)
        elif re.search(r'\(3\)', reasbm):
            phrase = self.post_proc(decomp.group(3))
            return re.sub(r'\(3\)', phrase, reasbm)
        else:
            return reasbm
