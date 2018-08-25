import threading
import time
from configparser import ConfigParser
from pathlib import Path
from threading import Thread

import numpy
import scipy.io.wavfile as wav
from numpy.lib import stride_tricks
from matplotlib import pyplot as plt
from pydub import AudioSegment
import os

config = ConfigParser()
config.read('config.ini')


def split_songs_into_chunks(from_path, to_path, from_format="mp3", to_format="mp3", chunk_size_in_seconds=5):
    for dirpath, dirs, files in os.walk(from_path):
        for file in files:
            if file.endswith(".mp3"):
                # only need last 3 chars of the path b/c data is split into 3 digit folders
                file_path = Path(os.getcwd(), from_path, dirpath[-3:], file)

                sound = AudioSegment.from_file(file_path, format=from_format)
                file_name = file[:-4]
                # file_handle = sound.export(Path(wav_folder, file_name+".wav"), format="wav")
                # file_handle = sound.export(Path(mp3_split, file_name+".mp3"), format="mp3")

                # don't create too many threads
                while threading.active_count() > 10:
                    print("Currently: ", threading.active_count(), " threads alive")
                    time.sleep(3)

                # create a thread and run it
                t = Thread(target=chunk_song, args=(sound, file_name, to_path, to_format, chunk_size_in_seconds))
                t.start()


def chunk_song(sound, file_name, to_path, to_format, chunk_size_in_seconds):
    # splitting training data into 5-second slices
    for i, chunk in enumerate(sound[::chunk_size_in_seconds * 1000]):
        file_path = Path(to_path, file_name + "_" + str(i) + "." + to_format)
        if not os.path.isfile(file_path):
            with open(file_path, "wb") as f:
                chunk.export(f, format=to_format)

    print("Finished chunking song: ", file_name)


def convert_mp3_to_wav_helper(from_path, to_path, threadcount=4):
    # grab all of the files, split into number of threads then do the work
    for dirpath, dirs, files in os.walk(from_path):
        data = numpy.array_split(files, threadcount)

        i = 0
        while i < threadcount:
            t = Thread(target=convert_mp3_to_wav, args=(dirpath, from_path, to_path, data[i]))
            t.start()
            i += 1


def convert_mp3_to_wav(dirpath, from_path, to_path, data):
    for file in data:
        if file.endswith(".mp3"):
            file_path = Path(os.getcwd(), from_path, file)
            file_name = file[:-4]
            file_name_wav = Path(to_path, file_name + ".wav")

            if not os.path.isfile(file_name_wav):
                # only need last 3 chars of the path b/c data is split into 3 digit folders
                sound = AudioSegment.from_file(file_path, format="mp3")

                sound.export(file_name_wav, format="wav")

                print("Finished converting song: ", file, " to wav format.")


def split_song_into_chunks(songPath, songName, sliceSize=10000, format="mp3"):
    sound = AudioSegment.from_file("/path/to/sound.wav", format=format)
    slices = sound[::sliceSize]
    return slices


def convert_song_to_mono_channel(songPath):
    sound = AudioSegment.from_file("sound1.wav")

    channel_count = sound.channels

    if channel_count > 1:
        print(songPath+" has 2 channels")
    else:
        print(songPath+" has 1 channel")
