# -*- coding: utf-8 -*-
# 基于solr+mongo的检索系统，对数据增/删/改在mongo上进行，检索时使用solr

import json

import pysolr

from logger import BaseLogger
from utils import seg_doc_with_search, unicode2str
from config import SOLR_CORE_MAP, SOLR_DEFAULT_ROWS


class SolrAPIHandler(BaseLogger):
    def __init__(self, core_name, **kwargs):
        self.core_name = core_name
        self.core = SOLR_CORE_MAP.get(core_name)
        self.solr_client = pysolr.Solr(self.core)
        super(SolrAPIHandler, self).__init__(**kwargs)

    def _seg_words(self, sentence):
        words = seg_doc_with_search(sentence)
        return words

    def search_index(self, query_str, **kwargs):
        self.debug("need_query_seg=False, query_str=%s, kwargs=%s", query_str, json.dumps(kwargs, ensure_ascii=False))
        return self.solr_client.search(query_str.encode("utf-8"), **kwargs)

    def search_with_seg(self, query, **kwargs):
        self.debug("need_query_seg=True")
        words_list = self._seg_words(unicode2str(query))
        self.debug("query seg result=%s", json.dumps(words_list, ensure_ascii=False))
        query_fields = kwargs.get("query_fields", [])
        rows = kwargs.get("rows", SOLR_DEFAULT_ROWS)
        if query_fields:
            query_list = list()
            for field in query_fields:
                field += ':'
                query_str = "(" + " ".join([field + word for word in words_list]) + ")"
                query_list.append(query_str)
        else:
            query_list = ["(" + " ".join(["*:" + word for word in words_list]) + ")"]
        q = "(%s)" % (" ".join(query_list))
        self.debug("core=%s query_str='%s'", self.core_name, q)
        docs = self.solr_client.search(q, rows=rows)
        return docs

if __name__ == "__main__":
    solr_api = SolrAPIHandler("biology-template")
    docs = solr_api.search_with_seg(u"胚是如何形成的", query_fields=['key_index'])
    for doc in docs:
        print doc.get('pattern', '')
        print doc.get('key_index', '')
        print doc.get('predicate_value', '')

    print "#" * 100
    docs = solr_api.search_index(query_str=u"*:*")
    for doc in docs:
        print doc
