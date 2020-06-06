import logging

from chatbot.common.configuration import Configuration
from chatbot.retriever.retriever import Retriever
from chatbot.reader.reader import Reader


class ChatBot:
    """ChatBot
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing " + __name__)

        # initialize everything
        self.config = Configuration()
        self.retriever = Retriever(self.config.retriever_config)
        self.reader = Reader()

    def process(self, query):
        """Process user input
        """
        docs = self.retriever.search(query)
        answer = self.reader.answer(query, docs[0])

        return answer
