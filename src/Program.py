import threading
import time
from configparser import ConfigParser
from threading import Thread

import config
import numpy
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


music_path = Path(os.getcwd(), config['PATHS']['TrackFolder'])
wav_folder = Path(os.getcwd(), config['PATHS']['WavFolder'])
mp3_split = Path(os.getcwd(), config['PATHS']['Mp3SplitFolder'])
spec_folder = Path(os.getcwd(), config['PATHS']['SpecFolder'])


def create_spectrogram_helper(from_path, to_path, threadcount=4):

    for dirpath, dirs, files in os.walk(from_path):
        for file in files:
        #if not dirpath.endswith("complete"):
            data = numpy.array_split(files, threadcount)
            wav_file_path = Path(os.getcwd(), from_path, file)

            # # don't create too many threads
            # while threading.active_count() > 2:
            #     print("Currently: ", threading.active_count(), " threads alive")
            #     time.sleep(3)
            #
            # i = 0
            # while i < threadcount:
            #     t = Thread(target=create_spectrogram, args=(wav_file_path, to_path))
            #     t.start()
            #     i += 1

            sound = AudioSegment.from_file(wav_file_path, format="wav")
            channel_count = sound.channels

            if channel_count is 2:
                sound.set_channels(1)

            filename = str(wav_file_path)[:-4] + "_tests.wav"
            sound.export(filename, format="wav")
            create_spectrogram(filename, to_path)


def create_spectrogram(file_path, to_path):
    sample_rate, samples = wavfile.read(Path(file_path))
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

    #dBS = 10*numpy.log10(spectrogram) # converting to dB
    #plt.pcolormesh(times, frequencies, dBS)

    plt.pcolormesh(times, frequencies, spectrogram)
    plt.imshow(spectrogram)
    plt.show()
    #plt.imsave()


def split_into_chunks():
    # t1 = Thread(target=split_songs_into_chunks, args=(music_path, mp3_split))
    # t1.start()

    t2 = Thread(target=convert_mp3_to_wav_helper, args=(mp3_split, wav_folder, 29))
    t2.start()

    # t1.join()
    t2.join()


def get_genre_dict():
    reader = DataReader(config)
    genres = reader.load_genres()


    genreDict = []

    for index in range(len(genres.title)):
        tup = (genres.title[index], genres.numtracks[index])
        genreDict += tup
        #print(index, genreDict[index])

    print(genreDict)


create_spectrogram_helper(wav_folder, spec_folder, 1)
