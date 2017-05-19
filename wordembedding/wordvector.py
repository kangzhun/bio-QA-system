# -*- coding: utf-8 -*-
import os

import time
from gensim.models import word2vec

from config import HERE


def load_embedding_txt(embedding_file_path, test_list):
    # 加载词向量
    model = word2vec.Word2Vec.load_word2vec_format(embedding_file_path)
    for item in test_list:
        similar_list = model.similar_by_word(item, topn=50)
        for (simi_word, simi_score) in similar_list:
            print simi_word
            print simi_score


def train_embedding(model_path, corpus_path, dimension, window, min_count):
    # 训练词向量
    sentences = word2vec.Text8Corpus(corpus_path)
    model = word2vec.Word2Vec(sentences, size=dimension, window=window, min_count=min_count)
    model.save(model_path)


def get_similarity(model_path, word):
    # 获取相似单词
    model = word2vec.Word2Vec.load(model_path)
    similar_list = model.similar_by_word(word, topn=50)
    for (simi_word, simi_score) in similar_list:
        print simi_word
        print simi_score

if __name__ == '__main__':
    # 训练词向量
    str_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    corpus_path = os.path.join(HERE, "data/corpus/seg_biology_book.txt")
    dimension = 300
    window = 8
    min_count = 0
    model_path = os.path.join(HERE, "data/word_embedding/w2v_%s_dim_%s.vec" % (str_time, dimension))
    train_embedding(model_path, corpus_path, dimension, window, min_count)

    # 加载词向量并测试
    model_path = os.path.join(HERE, "data/word_embedding/w2v_2017-05-02_18:06:22_dim_100.vec")

    # 获取相似单词
    get_similarity(model_path, u"生物")
