# ChatBot

ChatBot is an open-domain question answering chatbot.
ChatBot answers questions using a corpus of indexed documents i.e. it tries to find a document containing answer for a given question and then identifies answer from the text.

## Contents

- [Prerequisites](#prerequisites)
- [Installation](#installing-chatbot)
- [Quickstart](#quickstart)
- [Indexing Documents](#indexing-documents)

## Prerequisites

Required:
* Elasticsearch 7.7.x (https://www.elastic.co/downloads/elasticsearch)

Recommended:
* Anaconda 3.x (https://www.anaconda.com/products/individual)

**Remark**: recommended installation method, which is described in this section below, is based on usage of Conda environment. If you don't want to use Anaconda you can install Python 3.6 and all required dependencies listed in [environment.yml](environment.yml) instead, but this approach is not covered in current version of installation instructions.

## Installing ChatBot

1. Run the following commands to clone the repository and create Conda environment:
    ```bash
    git clone https://github.com/olegfaust/chatbot.git
    cd chatbot
    conda env create -f environment.yml
    ```

2. Setup retriever configuration ([config/retriever.ini](config/retriever.ini)) if needed. If you have installed Elasticsearch locally and didn't change its default settings, no changes are needed (just leave everything "as is").

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

run.sh/run.bat will start interactive session.
Type in your question, and chatbot will try to answer it. 

Example dialogue:
```
Q:>What is NLP?
A:> natural language processing
Q:>What is natural langiage processing?
A:> a subfield of linguistics, computer science, information engineering, and artificial intelligence
Q:>When was NLP invented?
A:> 1950s
```

Naturally, answers produced by ChatBot may be sometimes vague, doubtful or even entirely wrong:
```
Q:>Who was the inventor of NLP?
A:> alan turing
Q:>Who was Alan Turing?
A:> computing machinery and intelligence which proposed what is now called the turing test as a criterion of intelligence
```

If Chatbot is unable to answer a question, it will return an "empty" answer: 

```
Q:>Who was William Shakespeare?
A:> 
Q:>What is the difference between New York and New York City?
A:>
```

Chatbot can answer only those questions which subjects are covered in indexed documents.
`example_index.sh` indexes [data/small.csv](data/small.csv), which contains short passages
about NLP (Natural Language Processing), ML (Machine learning), Decision Tree and Logistic Regression.
You can add your own documents to search index if you want as it is described in the section below.

## Indexing documents

You can add documents to ChatBot search index either with [build_index.py](scripts/build_index.py) script or via any of Elasticsearch interfaces.

To add documents to search index with `build_index.py` script just pass a path to `.csv` file with documents to index as its argument.
For instance, to index example data provided with ChatBot source code, run:
 
```bash
python3 scripts/build_index.py data/small.csv
```

File passed to `build_index.py` script must be a valid comma-delimited `.csv` file with documents represented as rows, and `text` column containing document text for each row/document to be indexed (example: [data/small.csv](data/small.csv)).
There may be other columns in a `.csv` file as well, but only `text` column will be put into Elasticsearch index.

If you decided to add documents directly to Elasticsearch, check that you use the same Elasticsearch instance and index as
it is defined in [retriever.ini](config/retriever.ini) configuration file.
Put text of your documents into index field named `content`.
