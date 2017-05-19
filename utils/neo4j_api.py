# -*- coding: utf-8 -*-
from py2neo import authenticate, Graph
from pymongo import MongoClient

from config import NEO4J_HOST_PORT, NEO4J_USER, NEO4J_PWD, NEO4J_URL, MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME, \
    MONGODB_BIOLOGY_PROPERTY
from const import BIO_CYPER_TEMPLATE
from utils.logger import BaseLogger


class BioKnowledgeDB(BaseLogger):
    def __init__(self, **kwargs):
        super(BioKnowledgeDB, self).__init__(**kwargs)
        authenticate(NEO4J_HOST_PORT, NEO4J_USER, NEO4J_PWD)
        self.graph = Graph(NEO4J_URL)
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client.get_database(MONGODB_DBNAME)
        self.property_collection = db.get_collection(MONGODB_BIOLOGY_PROPERTY)

    def search_node_info(self, name, **kwargs):
        data = None
        node_property = kwargs.get('node_property', '')
        self.debug('>>> start search_node_info <<<')
        self.debug('search node name=%s, property=%s', name, node_property)
        if name and node_property:
            condition = BIO_CYPER_TEMPLATE['node_property'] % (name, node_property)
            data = self.graph.run(condition).data()
            self.debug('got property_value=%s', data)
            if not data:
                self.debug('search equal node name=%s, property=%s', name, node_property)
                condition = BIO_CYPER_TEMPLATE['equal_node_property'] % (name, node_property)
                data = self.graph.run(condition).data()
                self.debug('got property_value=%s', data)
        else:
            self.warn('@@@@@@@@@@@@@@ unexpected value!!!!!!')
        self.debug('>>> end search_node_info <<<')
        return data

    def return_neighbors_info(self, name, relationship, **kwargs):
        data = None
        node_property = kwargs.get('node_property', '')
        if node_property:
            self.debug('search node name=%s, relationship=%s, property=%s',
                       name, relationship, node_property)
        else:
            self.debug('search node name=%s, relationship=%s', name, relationship)
        if name:
            if node_property:
                condition = BIO_CYPER_TEMPLATE['neighbors_property'] % \
                            (name, relationship, node_property)
            else:
                condition = BIO_CYPER_TEMPLATE['neighbors_data'] % \
                            (name, relationship)
            data = self.graph.run(condition).data()
            self.debug('got neighbors_info=%s', data)
        else:
            self.warn('@@@@@@@@@@@@@@ unexpected name is None')
        return data

    def search(self, subject, predicate):
        ret = ''
        predicate_doc = self.property_collection.find_one({'uri': predicate})
        if predicate_doc:
            predicate_type = predicate_doc.get('type', '')
            self.debug('predicate_type=%s', predicate_type)
            if predicate_type == 'data_relationship':
                ret = self.search_node_info(subject, node_property=predicate)
            elif predicate_type == 'object_relationship':
                ret = self.return_neighbors_info(subject, predicate, node_property='name')
            else:
                self.warn('@@@@@@@@@@@@@@@@@@@@@@@@ unexpected predicate_type is None')
        else:
            self.warn('@@@@@@@@@@@@@@@@@@@@ unexpected predicate=%s', predicate)
        if ret:
            ret = " ".join([item.values()[0] for item in ret])
        return ret


if __name__ == '__main__':
    knowledge_db = BioKnowledgeDB()
    ret = knowledge_db.search('桃花', 'common_consistedOf')
    print ret
