# -*- coding: utf-8 -*-
import os
import zipfile

import numpy as np
import h5py
from gensim.models import word2vec

from config import HERE


def export_data_h5(vocabulary, embedding_matrix, output='embedding.h5'):
    # 将gensim词向量转存为hdf5格式
    print "vocabulary size = %i" % len(vocabulary)
    f = h5py.File(output, "w")
    compress_option = dict(compression="gzip", compression_opts=9, shuffle=True)
    words_flatten = '\n'.join(vocabulary)
    f.attrs['vocab_len'] = len(vocabulary)
    dt = h5py.special_dtype(vlen=str)
    _dset_vocab = f.create_dataset('words_flatten', (1, ), dtype=dt, **compress_option)
    _dset_vocab[...] = [words_flatten]
    _dset = f.create_dataset('embedding', embedding_matrix.shape, dtype=embedding_matrix.dtype, **compress_option)
    _dset[...] = embedding_matrix
    f.flush()
    f.close()


def glove_export(embedding_file):
    with zipfile.ZipFile(embedding_file) as zf:
        for name in zf.namelist():
            vocabulary = []
            embeddings = []
            with zf.open(name) as f:
                for line in f:
                    vals = line.split(' ')
                    vocabulary.append(vals[0])
                    embeddings.append([float(x) for x in vals[1:]])
            print(set(map(len, embeddings)))
            export_data_h5(vocabulary, np.array(embeddings, dtype=np.float32), output=name + ".h5")


def w2v_export(embedding_file):
    # 加载gensim词向量文件，并保存为h5格式
    try:
        model = word2vec.Word2Vec.load(embedding_file)
    except Exception, e:
        print e
        model = word2vec.Word2Vec.load_word2vec_format(embedding_file)
    vocabulary = model.wv.vocab.keys()
    embeddings = []
    for word in vocabulary:
        embeddings.append(model[word])
    export_data_h5(vocabulary, np.array(embeddings, dtype=np.float32), output=embedding_file + ".h5")


def normalize_word(embedding_file):
    # 将词向量进行规范化
    model = word2vec.Word2Vec.load_word2vec_format(embedding_file)
    vocabulary = model.vocab
    embeddings = []
    distances = np.zeros(100)
    import math
    for word in vocabulary:
        for i in range(100):
            distances[i] += math.pow(model[word][i], 2)

    for i in range(100):
        distances[i] = math.sqrt(distances[i])

    for word in vocabulary:
        vec = model[word]
        for i in range(100):
            vec[i] = vec[i] / distances[i]
        embeddings.append(vec)
    export_data_h5(vocabulary, np.array(embeddings, dtype=np.float32), output=embedding_file + "_normalize.h5")

if __name__ == "__main__":
    path = os.path.join(HERE, "data/word_embedding/w2v_2017-05-02_18:06:22_dim_100.vec")
    w2v_export(path)
