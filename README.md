# ChatBot

ChatBot is an open-domain question answering chatbot. ChatBot answers questions using a corpus of indexed documents i.e. it tries to find a document containing answer for a given question and then identifies answer from the text.

## Contents

- [Prerequisites](#prerequisites)
- [Installation](#installing-chatbot)
- [Quickstart](#quickstart)

## Prerequisites

Required:
* Elasticsearch 7.7.x (https://www.elastic.co/downloads/elasticsearch)

Recommended:
* Anaconda 3.x (https://www.anaconda.com/products/individual)

**Remark**: recommended installation method, which is described in this section below, is based on usage of Conda environment. If you don't want to use Anaconda you can install Python 3.6 and all required dependencies listed in `environment.yml` instead, but this approach is not covered in current version of installation instructions.

## Installing ChatBot

1. Run the following commands to clone the repository and create Conda environment:
    ```bash
    git clone https://github.com/olegfaust/chatbot.git
    cd chatbot
    conda env create -f environment.yml
    ```

2. Setup retriever configuration (`config/retriever.ini`) if needed. If you have installed Elasticsearch locally and didn't change its default settings, no changes are needed (just leave everything "as is").

3. Run `conda activate chatbot`. 
    * This activates the `chatbot` environment
    * Do this each time you want to work with ChatBot
    * Run `conda deactivate` when you finished your work with ChatBot and it's environment isn't needed anymore

## Quickstart

Run Elasticsearch if it is not started yet:
```bash
cd TO_YOUR_ELASTICSEARCH_DIRECTORY
./bin/elasticsearch
```

To index example document corpus (it must be done only once before the first usage of ChatBot) from ChatBot directory run:

```bash
conda activate chatbot
./example_index.sh
```

To run chatbot:

```bash
conda activate chatbot
./run.sh
```
