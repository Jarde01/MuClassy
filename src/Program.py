from src.datautils.DataReader import DataReader
import src.datautils.Preprocessing as pp
import os


# reader = DataReader()
# genres = reader.load_genres()


# genreDict = {}
#
# for index in range(len(genres.title)):
#     #print(index, genres.title[index])
#     genreDict[index] = genres.title
#
# print(genreDict)


AUDIO_DIR = os.getcwd() + "data\\fma_small"

for subdir, dirs, files in os.walk(AUDIO_DIR):
    for file in files:
        if file.endswith(".mp3"):
            #pp.convert_song_to_mono_channel(file)
            print(file)

