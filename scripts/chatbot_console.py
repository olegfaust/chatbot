"""
Retriever interactive console
"""

import colorama
from termcolor import colored

from chatbot.chatbot import ChatBot

# On Windows, calling colorama.init() will filter ANSI escape sequences out of any text sent to stdout or stderr,
# and replace them with equivalent Win32 calls.
colorama.init()

# initialize chatbot
chatbot = ChatBot()

while True:
    # receive question
    print(colored('Q:>', "yellow"), end="")
    question = input().strip()
    # answer question
    answer = chatbot.process(question)
    print(colored("A:>", "yellow"), colored(answer, "green"))
