"""
A script to build document search index for ChatBot's Retriever
"""

import sys
import logging

from argparse import ArgumentParser

from pathlib import Path

from chatbot.common.configuration import Configuration
from chatbot.retriever.indexer import Indexer


def set_default_arguments_(parser: ArgumentParser):
    """Set default options and arguments to the CLI parser.

    Parameters
    ----------
        parser : argparse.ArgumentParser
            Argument parser to set default arguments to
    """
    parser.add_argument(
        "csv_path",
        help="path to csv file to be added to search index",
        default=None,
        type=str)


def parse_cmd_parameters_(args):
    """Parse command line parameters

    Parameters
    ----------
        args : list, [str]
            Command line parameters

    Returns
    ----------
        options : dict
            Parsed options dictionary
    """
    # create argument parser
    parser = ArgumentParser(description="Script to build search index for ChatBot")
    set_default_arguments_(parser)
    # parse options and transform them into common dictionary
    options = vars(parser.parse_args(args))
    # remove options with None values (if any)
    options = {k: v for k, v in options.items() if v is not None}
    return options


def execute_(options):
    """Execute document indexing with given options

    Parameters
    ----------
        options : dict
            indexing options
    """
    # initialize configuration
    config = Configuration()

    # set formatting and redirect logger output to console (stdout)
    fmt = logging.Formatter("%(asctime)s: [ %(message)s ]", "%m/%d/%Y %I:%M:%S %p")
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger = logging.getLogger("chatbot.retriever.indexer")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    # initialize indexer
    indexer = Indexer(config.retriever_config)
    # add documents to index
    csv_path = Path(options['csv_path'])
    indexer.add_to_index(csv_path)


def main(args):
    """Main entry point for external applications

    Parameters
    ----------
        args : [str]
            command line arguments
    """
    options = parse_cmd_parameters_(args)
    execute_(options)


if __name__ == "__main__":
    main(sys.argv[1:])
