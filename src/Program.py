from configparser import ConfigParser

from src.datautils.DataReader import DataReader
import src.datautils.Preprocessing as pp
import os
from pathlib import Path

config = ConfigParser()
config.read('config.ini')
print(config.sections())


# reader = DataReader()
# genres = reader.load_genres()


# genreDict = {}
#
# for index in range(len(genres.title)):
#     #print(index, genres.title[index])
#     genreDict[index] = genres.title
#
# print(genreDict)

music_path = config['DEFAULT']['TrackFolders']

for subdir, dirs, files in os.walk(Path(os.getcwd(), music_path)):
    for file in files:
        if file.endswith(".mp3"):
            #pp.convert_song_to_mono_channel(file)
            print(file)

