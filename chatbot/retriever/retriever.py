import logging

from configparser import ConfigParser

from elasticsearch import Elasticsearch


class Retriever:
    """Document retriever
    retrieves documents from search index according to given query
    """

    def __init__(self, config: ConfigParser):
        """
        Parameters
        ----------
            config : ConfigParser
                retriever configuration file parser
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing " + __name__)
        self.config = config

        # connecting to Elasticsearch
        elastic_config = self.config["ELASTICSEARCH"]
        host = elastic_config["Host"]
        port = elastic_config["Port"]
        self.logger.info("Connecting to Elasticsearch on host='%s', port='%s'" % (host, port))
        self.elastic = Elasticsearch(host=host, port=port)

        # Ping Elasticsearch
        if self.elastic.ping():
            self.logger.info("Elastic search ping was successful")
        else:
            self.logger.error("Elastic search ping ERROR!!!")

        self.index_name = self.config["ELASTICSEARCH"]["IndexName"]

    def search(self, query, top_hits=1):
        """Search for closest matches in Elasticsearch index
        """
        response = self.elastic.search(
            index=self.index_name,
            size=top_hits,
            body={
                "query": {
                    "match": {
                        "content": query
                    }
                }
            })

        # put all hits into a list
        results = []
        response_hits = response['hits']['hits']
        for hit in response_hits:
            results.append(hit['_source']['content'])

        return results
