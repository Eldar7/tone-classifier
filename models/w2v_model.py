#!/usr/bin/python
# -*- coding: utf-8 -*-

# global
import io
import json
from gensim.models.word2vec import Word2Vec
import numpy as np

# this
import utils

CONFIG_NAME = "model.conf"
CONFIG_WORD2VEC_BINARIES = "w2v_binaries"

with io.open(CONFIG_NAME, 'r') as f:
    config = json.load(f, encoding='utf-8')

w2v_models = []
for model_name in config[CONFIG_WORD2VEC_BINARIES]:
    w2v_models.append(Word2Vec.load(model_name))


def vectorizer(labeled_message, term_voc, doc_voc):
    """
    Vector builder

    Arguments:
    ---------
        labeled_message -- dictionary with the following fields:
                           {score, id, terms, features}
        term_voc -- vocabulary of terms
        doc_voc -- vocabulary of documents

    Returns
    ------
        vector -- {index1: value1, ... , indexN: valueN}
    """
    vector = {}

    terms = labeled_message['terms']
    for model_index, w2v_model in enumerate(w2v_models):

        w2v_vector = sum_w2v_vectors_for_all_terms(w2v_model, terms)

        term_voc.insert_terms([index2term(model_index, item_index)
                               for item_index in range(0, w2v_vector.size)])

        for w2v_index, w2v_value in enumerate(w2v_vector):
            term = index2term(model_index, w2v_index)
            index = term_voc.insert_term(term)
            vector[index] = w2v_value

    features = labeled_message['features']
    for feature_name in features.keys():
        index = term_voc.get_term_index(feature_name)
        vector[index] = features[feature_name]

    return vector


def sum_w2v_vectors_for_all_terms(w2v_model, terms):
    """
    Sum all vectors from Word2Vec model for all terms presented in model
    """
    w2v_vector = np.array([0] * w2v_model.vector_size, dtype=np.float32)
    for term in terms:
        if term in w2v_model:
            w2v_vector = w2v_vector + w2v_model[term]

    return w2v_vector


def index2term(model_index, item_index):
    return '$W2V_ITEM_{model}_{item}'.format(model=str(model_index),
                                             item=str(item_index))


utils.vectorization_core(vectorizer, init_term_vocabulary=False)
