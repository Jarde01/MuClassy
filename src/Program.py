from configparser import ConfigParser
from threading import Thread

import config
from pydub import AudioSegment
import os
from pathlib import Path
from src.datautils.Preprocessor import split_songs_into_chunks, convert_mp3_to_wav, convert_mp3_to_wav_helper

#AudioSegment.converter = "C:\\ffmpeg-win64\\bin\\ffmpeg.exe"
#AudioSegment.ffprobe = "C:\\ffmpeg-win64\\bin\\ffprobe.exe"

config = ConfigParser()
config.read('config.ini')


# reader = DataReader(config)
# genres = reader.load_genres()

#
# genreDict = []
#
# for index in range(len(genres.title)):
#     tup = (genres.title[index], genres.numtracks[index])
#     genreDict += tup
#     #print(index, genreDict[index])
#
# print(genreDict)

music_path = Path(os.getcwd(), config['PATHS']['TrackFolder'])
wav_folder = Path(os.getcwd(), config['PATHS']['WavFolder'])
mp3_split = Path(os.getcwd(), config['PATHS']['Mp3SplitFolder'])


t1 = Thread(target=split_songs_into_chunks, args=(music_path, mp3_split))
t1.start()

#t2 = Thread(target=convert_mp3_to_wav_helper, args=(mp3_split, wav_folder, 4))
#t2.start()

t1.join()
#t2.join()

