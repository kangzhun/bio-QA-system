# -*- coding: utf-8 -*-
from service.template_service import TemplateBot
from utils.logger import BaseLogger
from utils.neo4j_api import BioKnowledgeDB


class BotApi(BaseLogger):
    def __init__(self, query, **kwargs):
        super(BotApi, self).__init__(**kwargs)
        template_bot = TemplateBot(query, **kwargs)
        self.bots = [template_bot]
        self.knowledge_db = BioKnowledgeDB()

    def reply(self):
        pass
