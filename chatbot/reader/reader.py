from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import torch

import logging


class Reader:
    """Document reader
    reads specified document to answer given question i.e.
    tries to find an answer for the question in provided document context
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing " + __name__)

        self.logger.info("started initializing tokenizer")
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased', return_token_type_ids=True)
        self.logger.info("started initializing model")
        self.model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')
        self.logger.info("Reader initialized successfully")

    def answer(self, question, document):
        """
        Parameters
        ----------
            question : str
                question to be answered
            document : str
                document context to find answer in

        Returns
        ----------
            answer : str
                answer to the question or empty string if no answer was found
        """
        # encode question and document context
        encoding = self.tokenizer.encode_plus(question, document)
        input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

        # apply model
        start_scores, end_scores = self.model(torch.tensor([input_ids]), attention_mask=torch.tensor([attention_mask]))

        # retrieve answer as str
        ans_tokens = input_ids[torch.argmax(start_scores): torch.argmax(end_scores) + 1]
        answer_tokens = self.tokenizer.convert_ids_to_tokens(ans_tokens, skip_special_tokens=True)
        answer = self.tokenizer.convert_tokens_to_string(answer_tokens)

        return answer
