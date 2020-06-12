"""
Retriever interactive console
"""

import sys
import logging
import colorama

from termcolor import colored

from chatbot.chatbot import ChatBot


def redirect_to_console(name):
    """Redirect logger output to console

    Parameters
    ----------
        name : str
            name of logger which output should be redirected to console
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))


# On Windows, calling colorama.init() will filter ANSI escape sequences out of any text sent to stdout or stderr,
# and replace them with equivalent Win32 calls.
colorama.init()

# set formatting
fmt = logging.Formatter("%(asctime)s: [ %(message)s ]", "%m/%d/%Y %I:%M:%S %p")
console = logging.StreamHandler()
console.setFormatter(fmt)
# redirect retriever logger output to console (stdout)
redirect_to_console("chatbot.retriever.retriever")
# redirect reader logger output to console (stdout)
redirect_to_console("chatbot.reader.reader")
# redirect transformers output to console
redirect_to_console("transformers.modeling_utils")

# initialize chatbot
chatbot = ChatBot()

while True:
    # receive question
    print(colored('Q:>', "yellow"), end="")
    question = input().strip()
    # answer question
    answer = chatbot.process(question)
    print(colored("A:>", "yellow"), colored(answer, "green"))
