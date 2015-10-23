#!/usr/bin/env python
# -*- coding: utf-8 -*-


def main(chat_script_path):
    """Run the parser."""
    try:
        read_content = read_file(chat_script_path)
    except IOError:
        raise
    else:
        # Parses the content
        list_of_content = parse_chat_content(read_content)
        # Split the content in variables
        initial = pop_content_given_a_simple_entry_type(list_of_content,
                                                        'initial')
        final = pop_content_given_a_simple_entry_type(list_of_content, 'final')
        quit = pop_content_given_a_simple_entry_type(list_of_content, 'quit')
        pre = pop_content_given_a_simple_entry_type(list_of_content, 'pre')
        post = pop_content_given_a_simple_entry_type(list_of_content, 'post')
        synon = pop_content_given_a_simple_entry_type(list_of_content, 'synon')
        key = pop_content_of_key_entry_type(list_of_content)
        return initial, final, quit, pre, post, synon, key


def read_file(chat_script_path):
    """Open the file."""
    chat_script_file = open(chat_script_path)
    read_content = chat_script_file.read()
    chat_script_file.close()
    return read_content


def parse_chat_content(read_content):
    """Parse the read content, removing the format characters."""
    # Removes the encoding markup
    read_content = read_content.lstrip('\ufeff')
    # Removes whitespace and tabs from the strings
    # adding them to the result variable
    parsed_content = []
    for line in read_content.splitlines():
        line = line.strip(' \t')
        parsed_content.append(line)
    return parsed_content


def pop_content_given_a_simple_entry_type(list_of_content, entry_type):
    """Pop the values which start with the entry type."""
    result = []
    i = 0
    while i < len(list_of_content):
        if list_of_content[i].startswith(entry_type):
            content = list_of_content[i]
            content = content.split(":", 1)[1]
            content = content.strip()
            result.append(content)
            list_of_content.pop(i)
        else:
            i += 1
    return result


def pop_content_of_key_entry_type(list_of_content):
    """Return a list with sublists composed by 'key', 'decomp' and 'reasmb'."""
    # Iterates over the list of content, adding the 'key' entry type and
    # its childs to an list
    result = []
    i = 0
    while i < len(list_of_content):
        a_key_and_its_values = []
        # Get all the 'keys' markups and its childs
        if list_of_content[i].startswith('key'):
            a_key = list_of_content.pop(i)
            a_key = a_key.split(":", 1)[1]
            a_key = a_key.strip()
            a_key_and_its_values.append(a_key)
            # Get all the 'decomp' markups and its childs
            a_decomp_and_its_values = []
            while (list_of_content and
                   list_of_content[i].startswith('decomp')):
                a_decomp = list_of_content.pop(i)
                a_decomp = a_decomp.split(":", 1)[1]
                a_decomp = a_decomp.strip()
                a_decomp_and_its_values.append(a_decomp)
                # Get all the 'reasmb' markups
                a_reasmb_and_its_values = []
                while (list_of_content and
                       list_of_content[i].startswith('reasmb')):
                    a_reasmb = list_of_content.pop(i)
                    a_reasmb = a_reasmb.split(":", 1)[1]
                    a_reasmb = a_reasmb.strip()
                    a_reasmb_and_its_values.append(a_reasmb)
                # Add all 'reasmb' markups to the relative decomp
                a_decomp_and_its_values.append(a_reasmb_and_its_values)
            # Add all the 'decomp' makrups to the relative key
            a_key_and_its_values.append(a_decomp_and_its_values)
            # Append the gathered content to the list
            result.append(a_key_and_its_values)
        # Only increments the index i if doesn't found a key
        else:
            i += 1
    return result
