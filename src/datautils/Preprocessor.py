from configparser import ConfigParser
from pathlib import Path

import scipy.io.wavfile as wav
from numpy.lib import stride_tricks
from matplotlib import pyplot as plt
from pydub import AudioSegment
import os

config = ConfigParser()
config.read('config.ini')


def split_songs_into_chunks(from_path, to_path, chunkSizeInSeconds=5):
    for dirpath, dirs, files in os.walk(music_path):
        for file in files:
            if file.endswith(".mp3"):
                # only need last 3 chars of the path b/c data is split into 3 digit folders
                file_path = Path(os.getcwd(), music_path, dirpath[-3:], file)

                sound = AudioSegment.from_file(file_path, format="mp3")
                file_name = file[:-4]
                # file_handle = sound.export(Path(wav_folder, file_name+".wav"), format="wav")
                # file_handle = sound.export(Path(mp3_split, file_name+".mp3"), format="mp3")

                # splitting training data into 5-second slices
                for i, chunk in enumerate(sound[::chunkSizeInSeconds*1000]):
                    with open(Path(mp3_split, file_name + "_" + str(i) + ".mp3"), "wb") as f:
                        chunk.export(f, format="mp3")

                print("Finished chunking song: ", file_name)


def convert_mp3_to_wav(from_path, to_path):
    for dirpath, dirs, files in os.walk(from_path):
        for file in files:
            if file.endswith(".mp3"):
                # only need last 3 chars of the path b/c data is split into 3 digit folders
                file_path = Path(os.getcwd(), from_path, dirpath[-3:], file)
                sound = AudioSegment.from_file(file_path, format="mp3")
                file_name = file[:-4]

                sound.export(Path(to_path, file_name+".wav"), format="wav")


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
