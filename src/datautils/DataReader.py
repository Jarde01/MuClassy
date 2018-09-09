import os
from pathlib import Path

import IPython.display as ipd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as skl
import sklearn.utils, sklearn.preprocessing, sklearn.decomposition, sklearn.svm
import librosa
import librosa.display
import configparser


class DataReader:
    def __init__(self, configFile):
        # Load metadata and features.
        self.config = configFile


        '''
        self.tracks = pd.read_csv('tracks.csv')
        self.genres = pd.read_csv('genres.csv')
        self.features = pd.read_csv('features.csv')
        self.echonest = pd.read_csv('echonest.csv')


        #np.testing.assert_array_equal(self.features.index, self.tracks.index)
        assert self.echonest.index.isin(self.tracks.index).all()

        self.shapes = []
        self.shapes = self.tracks.shape, self.genres.shape, self.features.shape, self.echonest.shape
        print("Finished loading data\n")
        '''

    def load_tracks(self):
        print("Loading tracks csv")
        tracks = pd.read_csv(Path(self.config['PATHS']['Metadata'], self.config['FILES']['Tracks']))
        print("Finished loading tracks")
        return tracks

    def load_genres(self):
        print("Loading genres csv...")
        genres = pd.read_csv(Path(self.config['PATHS']['Metadata'], 'genres.csv'))
        print("Finished loading genres")
        return genres

    def genre_accessor(self):
        print('{} top-level genres'.format(len(self.genres['top_level'].unique())))
        self.genres.loc[self.genres['top_level'].unique()].sort_values('#tracks', ascending=False)

    def features_accessor(self):
        print('{1} features for {0} tracks'.format(*self.features.shape))
        columns = ['mfcc', 'chroma_cens', 'tonnetz', 'spectral_contrast']
        columns.append(['spectral_centroid', 'spectral_bandwidth', 'spectral_rolloff'])
        columns.append(['rmse', 'zcr'])
        for column in columns:
            ipd.display(self.features[column].head().style.format('{:.2f}'))

    def echonest_features(self):
        print('{1} features for {0} tracks'.format(*self.echonest.shape))
        ipd.display(self.echonest['echonest', 'metadata'].head())
        ipd.display(self.echonest['echonest', 'audio_features'].head())
        ipd.display(self.echonest['echonest', 'social_features'].head())
        ipd.display(self.echonest['echonest', 'ranks'].head())

    def load_audio(self):
        filename = utils.get_audio_path(self.AUDIO_DIR, 2)
        print('File: {}'.format(filename))

        x, sr = librosa.load(filename, sr=None, mono=True)
        print('Duration: {:.2f}s, {} samples'.format(x.shape[-1] / sr, x.size))

        start, end = 7, 17
        ipd.Audio(data=x[start * sr:end * sr], rate=sr)

    def librosa_spectrogram(self, x, sr, start, end):
        librosa.display.waveplot(x, sr, alpha=0.5);
        plt.vlines([start, end], -1, 1)

        start = len(x) // 2
        plt.figure()
        plt.plot(x[start:start + 2000])
        plt.ylim((-1, 1));

