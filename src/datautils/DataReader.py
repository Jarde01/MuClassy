import os

import IPython.display as ipd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as skl
import sklearn.utils, sklearn.preprocessing, sklearn.decomposition, sklearn.svm
import librosa
import librosa.display


class DataReader:
    def __init__(self):

        # Directory where mp3 are stored.
        curr = os.getcwd()
        os.chdir("data\\fma_metadata")

        # Load metadata and features.
        self.tracks = pd.read_csv('tracks.csv')
        self.genres = pd.read_csv('genres.csv')
        self.features = pd.read_csv('features.csv')
        self.echonest = pd.read_csv('echonest.csv')

        #np.testing.assert_array_equal(self.features.index, self.tracks.index)
        assert self.echonest.index.isin(self.tracks.index).all()

        self.shapes = []
        self.shapes = self.tracks.shape, self.genres.shape, self.features.shape, self.echonest.shape
        print("Finished loading data\n")

    def genre_accessor(self):
        print('{} top-level genres'.format(len(self.genres['top_level'].unique())))
        self.genres.loc[self.genres['top_level'].unique()].sort_values('#tracks', ascending=False)
