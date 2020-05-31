"""
Retriever interactive console
"""

import code

from chatbot.common.configuration import Configuration
from chatbot.retriever.retriever import Retriever

# initialize document retriever
config = Configuration()
retriever = Retriever(config.retriever_config)


def request(query, top_hits=1):
    print(retriever.search(query, top_hits))

# run console application
code.interact(
    banner="Interactive Retriever interface\n"
           "To retrieve documents type in 'request' function:\n"
           "request('your request here', number_of_top_documents)\n\n"
           "Usage example:\n"
           "request('What is natural language processing?', 2)\n",
    local=locals())
