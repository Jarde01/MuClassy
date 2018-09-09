import multiprocessing
import threading
import time
import wave
from configparser import ConfigParser
from multiprocessing.pool import Pool
from threading import Thread

import config
import numpy
import pylab
from pydub import AudioSegment
import os
from pathlib import Path

from src.datautils.DataReader import DataReader
from src.datautils.Preprocessor import split_songs_into_chunks, convert_mp3_to_wav, convert_mp3_to_wav_helper

import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

#AudioSegment.converter = "C:\\ffmpeg-win64\\bin\\ffmpeg.exe"
#AudioSegment.ffprobe = "C:\\ffmpeg-win64\\bin\\ffprobe.exe"

config = ConfigParser()
config.read('config.ini')
data_reader = DataReader(config)

music_path = Path(os.getcwd(), config['PATHS']['TrackFolder'])
wav_folder = Path(os.getcwd(), config['PATHS']['WavFolder'])
mp3_split = Path(os.getcwd(), config['PATHS']['Mp3SplitFolder'])
spec_folder = Path(os.getcwd(), config['PATHS']['SpecFolder'])


def create_spectrogram_helper(from_path, to_path, threadcount=4):
    i = 0
    for dirpath, dirs, files in os.walk(from_path):
        for file in files:
            wav_file_path = Path(os.getcwd(), from_path, file)

            # # don't create too many threads
            # while threading.active_count() > threadcount:
            #     print("Currently: ", threading.active_count(), " threads alive")
            #     time.sleep(3)
            #
            # t = Thread(target=graph_spectrogram, args=(wav_file_path, to_path))
            # t.start()
            graph_spectrogram(wav_file_path, to_path)


def graph_spectrogram(wav_file, to_path='data\\spectrograms'):
    spec_file_path = Path(to_path, str(Path(wav_file).name)[:-4] + '.png')
    if os.path.isfile(spec_file_path):
        print(Path(spec_file_path).name, " already exists")
    else:
        sound_info, frame_rate = get_wav_info(wav_file)
        fig = pylab.figure(num=None, frameon=False)
        fig.set_size_inches(20, 10)
        axis = pylab.Axes(fig, [0., 0, 1., 1.])
        axis.set_axis_off()
        fig.add_axes(axis)
        # pylab.specgram(sound_info, Fs=frame_rate)
        # larger values of NFFT will cause the middle freq to become to pronounced
        pylab.specgram(sound_info, Fs=frame_rate, NFFT=80, noverlap=64)
        pylab.savefig(spec_file_path)
        pylab.close()


def get_wav_info(wav_file):
    wav = wave.open(str(wav_file), 'r')
    # wav.setnchannels(1)
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'Int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate


def get_genre_dict():
    reader = DataReader(config)
    genres = reader.load_genres()

    genre_dict = []

    for index in range(len(genres.title)):
        tup = (genres.title[index], genres.numtracks[index])
        genre_dict += tup
        #print(index, genreDict[index])

    print(genre_dict)

#
# def multiprocess_spectrogram(from_path, to_path, workers=4):
#     i = 0
#     files = os.listdir(from_path)
#     p = multiprocessing.Pool(workers)
#     p.imap(graph_spectrogram, (Path(os.getcwd(), from_path, file) for file in files)
#
#     # wav_file_path = Path(os.getcwd(), from_path, file)
#
#     # don't create too many threads
#     while threading.active_count() > threadcount:
#         print("Currently: ", threading.active_count(), " threads alive")
#         time.sleep(3)
#
#     t = Thread(target=graph_spectrogram, args=(wav_file_path, to_path))
#     t.start()
#     # graph_spectrogram(wav_file_path, to_path)


def tag_files(from_path, to_path, threadcount=4):
    genres_df = data_reader.load_genres()
    genres_dict = genres_df.to_dict()

    tracks_df = data_reader.load_tracks()
    tracks_dict = tracks_df.to_dict()

    for dirpath, dirs, files in os.walk(from_path):
        for file in files:
            file_path = Path(os.getcwd(), from_path, file)

            # # don't create too many threads
            # while threading.active_count() > threadcount:
            #     print("Currently: ", threading.active_count(), " threads alive")
            #     time.sleep(3)
            #
            # t = Thread(target=rename_file_with_genre, args=(file_path, genres_dict, tracks_dict))
            # t.start()
            rename_file_with_genre(file_path, genres_dict, tracks_dict)


def rename_file_with_genre(file_path, genres_dict, tracks_dict):
    tokens = Path(file_path).name.split('_')
    id = tokens[0].lstrip('0')

    try:
        x = tracks_dict[id]
    except:
        print(id, "Key error")
        
    print(tokens)


tag_files(spec_folder, spec_folder, threadcount=10)
# create_spectrogram_helper(wav_folder, spec_folder, threadcount=10)
# multiprocess_spectrogram(wav_folder, spec_folder, workers=10)
