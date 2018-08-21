import scipy.io.wavfile as wav
from numpy.lib import stride_tricks
from matplotlib import pyplot as plt
from pydub import AudioSegment
import os


def mp3_to_wav(songPath, songName):
    sound = AudioSegment.from_file(songPath, format="mp3")
    cwd = os.getcwd()

    #file_handle = sound.export(path, format="wav"))

    cwd = os.getcwd()
    #sound.export("")


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
