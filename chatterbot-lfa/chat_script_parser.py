#!/usr/bin/env python
# -*- coding: utf-8 -*-


def main(chat_script_path):
    """Run the parser."""
    try:
        read_content = read_file(chat_script_path)
    except IOError:
        raise
    else:
        list_of_content = parse_chat_content(read_content)

        initial = pop_content_given_a_simple_entry_type(list_of_content, 'initial')
        final = pop_content_given_a_simple_entry_type(list_of_content, 'final')
        quit = pop_content_given_a_simple_entry_type(list_of_content, 'quit')
        pre = pop_content_given_a_simple_entry_type(list_of_content, 'pre')
        post = pop_content_given_a_simple_entry_type(list_of_content, 'post')
        synon = pop_content_given_a_simple_entry_type(list_of_content, 'synon')
        key = pop_content_of_key_entry_type(list_of_content)

        initial = remove_label_from_simple_entry_types(initial)
        final = remove_label_from_simple_entry_types(final)
        quit = remove_label_from_simple_entry_types(quit)
        pre = remove_label_from_simple_entry_types(pre)
        post = remove_label_from_simple_entry_types(post)
        synon = remove_label_from_simple_entry_types(synon)
        # key

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
            result.append(list_of_content[i])
            list_of_content.pop(i)
        else:
            i += 1

    return result


def pop_content_of_key_entry_type(list_of_content):
    """Return a list with sublists composed by 'key', 'decomp' and 'reasmb'."""
    # Iterates over the list of content, adding the 'key' entry type and
    # its childs to an list
    list_of_keys = []
    i = 0
    while i < len(list_of_content):
        a_key_and_its_values = []

        # Get all the 'keys' markups and its childs
        if list_of_content[i].startswith('key'):
            a_key_and_its_values.append(list_of_content[i])
            list_of_content.pop(i)

            # Get all the 'decomp' markups and its childs
            while (list_of_content and
                   list_of_content[i].startswith('decomp')):
                a_key_and_its_values.append(list_of_content[i])
                list_of_content.pop(i)

                # Get all the 'reasmb' markups
                while (list_of_content and
                       list_of_content[i].startswith('reasmb')):
                    a_key_and_its_values.append(list_of_content[i])
                    list_of_content.pop(i)

            # Append the popped content to the final list
            list_of_keys.append(a_key_and_its_values)

        # Only increments the index i if doesn't found a key
        else:
            i += 1

    return list_of_keys


def remove_label_from_simple_entry_types(entry_type):
    """Strips the entry type label from the list item."""
    result = []
    for item in entry_type:
        # Splits the file in label and content and append only the content
        item = item.split(":",1)[1]
        item = item.lstrip()
        result.append(item)

    return result
