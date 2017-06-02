# -*- coding: utf-8 -*-
# 基于模板的问答
import json
import re

from utils import str2unicode, unicode2str
from utils.logger import BaseLogger
from utils.neo4j_api import BioKnowledgeDB
from utils.solr_api import SolrAPIHandler


class TemplateBot(BaseLogger):
    def __init__(self, **kwargs):
        super(TemplateBot, self).__init__(**kwargs)
        self.query = ''
        self.template_core = SolrAPIHandler("biology-template")  # solr问句模板core
        self.triple_core = SolrAPIHandler("biology-triple")  # solr三元组core
        self.knowledge_db = BioKnowledgeDB()  # 生物基础学科知识图谱

    def _match_predicate(self):
        self.debug('>>> start _match_predicate <<<')
        templates_docs = self.template_core.search_with_seg(self.query, query_fields=['key_index'],)
        templates_list = list(templates_docs)
        predicate_ret = ''
        subject_ret = ''
        self.debug("got templates_docs=%s", json.dumps(templates_list, ensure_ascii=False))
        if templates_list:
            for tmp_item in templates_list:
                pattern_str = tmp_item.get('pattern', '')
                predicate_value = tmp_item.get('predicate_value', '')
                if pattern_str and predicate_value:
                    pattern = re.compile(ur'%s' % pattern_str)
                    is_match = pattern.match(str2unicode(self.query))
                    if is_match:
                        self.debug('got match pattern=%s, predicate_value=%s',
                                   pattern_str, predicate_value)
                        subject_ret = is_match.group('title')
                        predicate_ret = predicate_value
                        return subject_ret, predicate_ret
                else:
                    self.warn('@@@@@@@@@@@@@@@@@@@@@@@ unexpected pattern_str=%s, predicate_value=%s',
                              pattern_str, predicate_value)
        else:
            self.debug("retrieved None templates_docs")
        self.warn("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ don't match any templates ")
        self.debug(">>> end _match_predicate <<<")
        return subject_ret, predicate_ret

    def _match_subject(self, subject_str):
        self.debug('>>> start _match_subject <<<')
        triple_docs = self.triple_core.search_with_seg(subject_str,
                                                       query_fields=['triple_subject_index'], rows=1)
        triple_list = list(triple_docs)
        subject_ret = ''
        self.debug("got triple_docs=%s", json.dumps(triple_list, ensure_ascii=False))
        if triple_list:
            subject_ret = triple_list[0].get('triple_subject', '')
            self.debug("got subject=%s", subject_ret)
        else:
            self.debug("retrieved None triple_docs")
        self.debug(">>> end _match_subject <<<")
        return subject_ret

    def reply(self, query):
        """
        根据query返回答案
        :param query: 用户输入问句
        :return: 答案
        """
        answer = {}
        self.query = unicode2str(query).strip()
        self.debug("[ start ] query=%s", self.query)
        if self.query:
            subject_str, predicate = self._match_predicate()  # 匹配谓语, 并把主语部分返回，用于后续检索主语
            if subject_str:
                self.debug('got subject_str=%s, predicate=%s', subject_str, predicate)
                subject = self._match_subject(subject_str)
                if not subject:
                    self.warn('@@@@@@@@@@@@@@@@@@@ unexpected subject')
                elif not predicate:
                    self.warn('@@@@@@@@@@@@@@@@@@@ unexpected predicate')
                else:
                    self.debug('start search knowledge_db with subject=%s, predicate=%s', subject, predicate)
                    answer = self.knowledge_db.search(subject=subject, predicate=predicate)
            else:
                self.warn('@@@@@@@@@@@@@@@@@@@ unexpected subject_str is None')
        else:
            self.warn("@@@@@@@@@@@@@@@@@@@ unexpected query is None")
        if answer:
            ret = []
            for key in answer.keys():
                ret.append(' '.join(answer[key]))
            ret = '\n'.join(ret)
        else:
            ret = ''
        return ret
