from src.datautils.DataReader import DataReader

reader = DataReader()
genres = reader.load_genres()


genreDict = {}

for index in range(len(genres.title)):
    #print(index, genres.title[index])
    genreDict[index] = genres.title

print(genreDict)
