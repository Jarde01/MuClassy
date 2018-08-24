from configparser import ConfigParser
from pydub import AudioSegment
from src.datautils.DataReader import DataReader
import src.datautils.Preprocessing as pp
import os
from pathlib import Path

AudioSegment.converter = "C:\\ffmpeg-win64\\bin"

config = ConfigParser()
config.read('config.ini')
print(config.sections())


reader = DataReader(config)
genres = reader.load_genres()


genreDict = []

for index in range(len(genres.title)):
    tup = (genres.title[index], genres.numtracks[index])
    genreDict += tup
    #print(index, genreDict[index])

print(genreDict)


music_path = config['DEFAULT']['TrackFolders']
numFiles = 0
wav_folder = Path(os.getcwd(), "data\\wav_files")

for dirpath, dirs, files in os.walk(music_path):
        for file in files:
            if file.endswith(".mp3"):
                if numFiles < 10:
                    # only need last 3 chars of the path b/c data is split into 3 digit folders
                    sound = AudioSegment.from_file(Path(os.getcwd(), music_path, dirpath[-3:], file), format="mp3")
                    fileName = file=file[:-4]
                    new_file = sound.export(Path(wav_folder, fileName, "wav"), format="wav")
                    #pp.convert_song_to_mono_channel(file)
                    #print(file)
                    numFiles += 1
                else:
                    break

#print("There are "+str(numFiles)+" tracks")
