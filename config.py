# -*- coding: utf-8 -*-
import os

HERE = os.path.abspath(os.path.dirname(__file__))

# logger config
LOGGER_PATH = HERE
LOGGER_NAME = "bio_qa.log"

# solr config
SOLR_HOST = "127.0.0.1"
SOLR_PORT = 8983
SOLR_SERVER = "http://%s:%s/solr" % (SOLR_HOST, SOLR_PORT)

BIOLOGY_TRIPLE_CORE_NAME = "biology-triple"
BIOLOGY_TRIPLE_CORE = "/".join([SOLR_SERVER, BIOLOGY_TRIPLE_CORE_NAME])

BIOLOGY_QA_CORE_NAME = "biology-qa"
BIOLOGY_QA_CORE = "/".join([SOLR_SERVER, BIOLOGY_QA_CORE_NAME])

BIOLOGY_TEMPLATE_CORE_NAME = "biology-template"
BIOLOGY_TEMPLATE_CORE = "/".join([SOLR_SERVER, BIOLOGY_TEMPLATE_CORE_NAME])

SOLR_CORE_MAP = {
    BIOLOGY_TRIPLE_CORE_NAME: BIOLOGY_TRIPLE_CORE,
    BIOLOGY_QA_CORE_NAME: BIOLOGY_QA_CORE,
    BIOLOGY_TEMPLATE_CORE_NAME: BIOLOGY_TEMPLATE_CORE,
}

SOLR_DEFAULT_ROWS = 50

# jieba_config
CUSTOM_DICTIONARY_PATH = os.path.join(HERE, "data/corpus", "custom_dictionary.txt")

# neo4j config
NEO4J_HOST_PORT = "localhost:7474"
NEO4J_USER = "kangzhun"
NEO4J_PWD = "741953"
NEO4J_URL = "http://localhost:7474/db/data/"

# mongodb config
MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DBNAME = "biology-db"
MONGODB_BIOLOGY_TRIPLE = "biology-triple"
MONGODB_BIOLOGY_QA = "biology-qa"
MONGODB_BIOLOGY_TEMPLATE = "biology-template"
MONGODB_BIOLOGY_PROPERTY = 'biology-property'
