from configparser import ConfigParser

import config
from pydub import AudioSegment
import os
from pathlib import Path
from src.datautils.Preprocessor import split_songs_into_chunks


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


split_songs_into_chunks(from_path=music_path, to_path=mp3_split)
