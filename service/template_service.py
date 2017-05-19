# -*- coding: utf-8 -*-
# 基于模板的问答
import json
import re

from utils import str2unicode
from utils.logger import BaseLogger
from utils.neo4j_api import BioKnowledgeDB
from utils.solr_api import SolrAPIHandler


class TemplateBot(BaseLogger):
    def __init__(self, query, **kwargs):
        super(TemplateBot, self).__init__(**kwargs)
        self.query = query
        self.debug("[ start ] query=%s", self.query)
        self.template_core = SolrAPIHandler("biology-template")
        self.triple_core = SolrAPIHandler("biology-triple")
        self.knowledge_db = BioKnowledgeDB()

    def _match_predicate(self):
        self.debug('>>> start _match_predicate <<<')
        templates_docs = self.template_core.search_with_seg(self.query.strip(), query_fields=['key_index'])
        templates_list = list(templates_docs)
        predicate_ret = ''
        subject_ret = ''
        self.debug("got templates_docs=%s", json.dumps(templates_list, ensure_ascii=False))
        if templates_list:
            for item in templates_list:
                pattern_str = item.get('pattern', '')
                predicate_value = item.get('predicate_value', '')
                if pattern_str and predicate_value:
                    pattern = re.compile(ur'%s' % pattern_str)
                    is_match = pattern.match(str2unicode(self.query))
                    if is_match:
                        self.debug('got match pattern=%s, predicate_value=%s',
                                   pattern_str, predicate_value)
                        subject_ret = is_match.group('title')
                        predicate_ret = predicate_value
                        break
                else:
                    self.warn('@@@@@@@@@@@@@@@@@@@@@@@ unexpected pattern_str=%s, predicate_value=%s',
                              pattern_str, predicate_value)
        else:
            self.debug("retrieved None templates_docs")
        self.debug(">>> end _match_predicate <<<")
        return subject_ret, predicate_ret

    def _match_subject(self, subject_str):
        self.debug('>>> start _match_subject <<<')
        triple_docs = self.triple_core.search_with_seg(subject_str.strip(),
                                                       query_fields=['triple_subject_index'], rows=1)
        triple_list = list(triple_docs)
        subject_ret = ''
        self.debug("got triple_docs=%s", json.dumps(triple_list, ensure_ascii=False))
        if triple_list:
            subject_ret = triple_list[0].get('triple_subject', '')
        else:
            self.debug("retrieved None triple_docs")
        self.debug(">>> end _match_subject <<<")
        return subject_ret

    def reply(self):
        answer = ''
        if self.query.strip():
            subject_str, predicate = self._match_predicate()
            if subject_str and predicate:
                self.debug('got subject_str=%s, predicate=%s', subject_str, predicate)
                subject = self._match_subject(subject_str)
                if subject and predicate:
                    self.debug('got subject=%s, predicate=%s', subject, predicate)
                    answer = self.knowledge_db.search(subject=subject, predicate=predicate)
                else:
                    self.warn('@@@@@@@@@@@@@@@@@@@ unexpected subject')
            else:
                self.warn('@@@@@@@@@@@@@@@@@@@ unexpected subject_str or predicate is None')
        else:
            self.warn("@@@@@@@@@@@@@@@@@@@ unexpected query is None")
        return answer


if __name__ == '__main__':
    template_bot = TemplateBot("桃花由什么组成")
    answer = template_bot.reply()
    print answer
