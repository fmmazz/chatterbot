import sys

import chatterbot
import chat_script_parser


def main(chat_script_path):
    """Run the main logic of the program."""
    try:
        initial, final, quit, pre, post, synon, key = \
            chat_script_parser.main(chat_script_path)
    except IOError:
        print("File not found. End of the program.")
    else:
        AChatterBot = chatterbot.ChatterBot(initial, final, quit, pre, post,
                                            synon, key)
        AChatterBot.start_chat()

if __name__ == '__main__':
    chat_script = sys.argv[1]
    main(chat_script)
