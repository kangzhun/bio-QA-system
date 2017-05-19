# -*- coding: utf-8 -*-
# 自然语言处理工具包
import jieba
import jieba.posseg as pseg

from config import CUSTOM_DICTIONARY_PATH
from utils.logger import BaseLogger


class JiebaClient(BaseLogger):
    def __init__(self, custom_dict_path=CUSTOM_DICTIONARY_PATH,**kwargs):
        super(JiebaClient, self).__init__(**kwargs)
        jieba.load_userdict(custom_dict_path)
        self.debug("init JiebaClient, with custom_dict_path=%s", custom_dict_path)

    def seg(self, doc):
        words = list()
        tags = list()
        self.debug("doc=%s", doc)
        for item in pseg.cut(doc):
            words.append(item.word)
            tags.append(item.flag)
        self.debug("words=%s, tags=%s", " ".join(words), " ".join(tags))
        return words, tags

    def seg_for_search(self, doc):
        words = list()
        for item in jieba.cut_for_search(doc):
            words.append(item)
        return words


if __name__ == '__main__':
    jieba_client = JiebaClient()
    words, tags = jieba_client.seg('你是谁')
    print " ".join(words)

    jieba_client.seg_for_search("胚是如何形成的")
