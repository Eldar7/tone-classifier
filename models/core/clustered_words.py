# -*- coding: utf-8 -*-

import io
import json
import os.path


class BagOfClustersFeature:

    PARAM_CLUSTERED_WORDS_FILEPATH = 'clustered_words_filepath'

    def __init__(self, unique_name, base_filepath, parameters):
        """
        Arguments
        ---------
            keyword_name -- feature unique name
            base_filepath -- filepath of feature config
            parameters -- lexicon parameters, presented by dictionary
        """
        self.unique_name = unique_name

        filepath = os.path.join(
            base_filepath,
            parameters[BagOfClustersFeature.PARAM_CLUSTERED_WORDS_FILEPATH])

        with io.open(filepath, 'r', encoding='utf-8') as f:
            self.clustered_words = json.load(f, encoding='utf-8')

    def vectorize(self, terms):
        """
        Produce features vector, bag of clusters for 'terms'

        Returns
        -------
            features -- {feature: value, ...}
        """
        features = {}
        for term in terms:
            if term in self.clustered_words:
                feature_name = self.__get_feature_name(
                    int(self.clustered_words[term]))
                if feature_name in features:
                    features[feature_name] += 1
                else:
                    features[feature_name] = 1

        return features

    def __get_feature_name(self, cluster_index):
        return '{name}_{cluster}'.format(name=self.unique_name,
                                         cluster=cluster_index)
