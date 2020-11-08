## Assignment for the Course Algorithms for Information Retrieval (UE17CS412)

### Team:
* Ashwin R. Bharadwaj
* Hardik Gourisaria
* Hrishikesh V
* K Shrinidhi Bhagavath

## Trie based inverted index


### Install Requirements

```bash
pip3 install -r requirements.txt
```


### Download required nltk data

```bash
python3 initialize.py
```

### How to use search engine

```bash
python3 main.py
```


### How to change search query parameter

Go to config.py in config directory.

#### Changeable configs:
 - DATA_PATH = Path to csv files
 - ENGINE_PATH = Path were data required by engine is stored
 - LOG_FILE = Path where log file is stored
 - RANKING = Boolean (True or False), specifies if you want to rank the output or not
 - SHOW_DETAIL = Boolean (True or False), specifies if you want to extract data from csv and show along with the result
 - RANKING_ALGO = Specifies type of ranking algorithm you want to adopt. Options = "cos", "match"
 - TOTAL_N_RESULT = Number of top results to be displayed

### Problem Statement
#### Problem:
 - a) Build a search engine for Environmental News NLP archieve.
 - b) Built a corpus for archieve with atleast 418 documents.

#### Data:
 a) Use the following link for Environmental News NLP dataset. https://www.kaggle.com/amritvirsinghx/environmental-news-nlp-dataset

### Deliverables: 
Your Code should contain functionality to 
 - Search for the terms in the query
 - Create Postings list
 - Fill the Inverted Index
 - Rank the pages
 - Retrieve the data from the dictionary
 - Query response time 
 - Measure the efficiency using precision,recall,F measure.
 
### Demo:
 - Run your code and carryout the search with different queries. 
 - Retrieve the data, compile and compare metrics with any one of the search engine  like Elasticsearch, Apache Solr,Apache Lucene, Google Cloud Search, Google Desktop Search for the same corpus.
 - Measure the efficiency.

### Report:
 - You should submit a hard copy, 4
 - page summary of your project 
 - Your report should include the code snippet/algorithm used, similarity check of retrieved data obtained with your search engine and any one search engine like Elasticsearch,Apache Solr, Apache Lucene, Google Cloud Search, Google Desktop Search.
 - Interpretation of efficiency.
Last para of your report should contain your observations on the Learning Outcomes of this project.
