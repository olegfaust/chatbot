import csv
import tqdm
import logging

from pathlib import Path
from configparser import ConfigParser

from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk


class Indexer:
    """Document indexer
    adds documents to search index
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

        index_name = self.config["ELASTICSEARCH"]["IndexName"]
        num_shards = self.config["ELASTICSEARCH"]["Shards"]
        num_replicas = self.config["ELASTICSEARCH"]["Replicas"]

        self.create_index_if_not_exist(index_name, num_shards, num_replicas)

    def create_index_if_not_exist(self, index_name, num_shards, num_replicas):
        """Creates an index in Elasticsearch if it isn't created yet."""
        if not self.elastic.indices.exists(index_name):
            index_settings = self.create_index_settings(num_shards, num_replicas)
            self.elastic.indices.create(index=index_name, body=index_settings)
            self.logger.info("Created index '%s'" % index_name)
        else:
            self.logger.info("Index '%s' already exists, no changes made" % index_name)

    def create_index_settings(self, num_shards, num_replicas):
        # Prepare index settings
        index_settings = {
            "settings": {
                "number_of_shards": num_shards,
                "number_of_replicas": num_replicas
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "content": {
                        "type": "text"
                    }
                }
            }
        }
        return index_settings

    def add_to_index(self, path: Path):
        self.logger.info("Adding '%s' to search index" % path)
        # check if path to add exists
        if not path.exists():
            self.logger.error("Path '%s' doesn't exist" % path)
            raise FileNotFoundError
        # run indexing
        encoding = self.config["DOCUMENT_PREPROCESSING"]["Encoding"]
        num_of_docs = sum(1 for line in path.open(encoding=encoding)) - 1  # -1 as the first row contains column titles
        progress = tqdm.tqdm(unit="docs", total=num_of_docs)
        index_name = self.config["ELASTICSEARCH"]["IndexName"]
        for ok, action in streaming_bulk(client=self.elastic, index=index_name,
                                         actions=self.generate_actions(path)):
            progress.update(1)

    def generate_actions(self, path: Path):
        """Generate iterator of actions to be sent to Elasticsearch
        Reads the provided file and for each row (i.e. document) in it yields a text to be indexed.
        """
        encoding = self.config["DOCUMENT_PREPROCESSING"]["Encoding"]

        with path.open(encoding=encoding) as f:
            reader = csv.DictReader(f)

            for row in reader:
                article = {
                    'content': row["text"]
                }
                yield article
