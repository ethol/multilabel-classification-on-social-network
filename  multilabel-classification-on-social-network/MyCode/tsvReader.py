import csv
from imdbMovie import movie
from lib import Helper
from algorithms import Algorithms
from datetime import datetime
import random
import copy



moviesRaw = []
sLine = []
genresCount = dict()
time = datetime.now()
crew = dict()
crewMember = dict()
movieEdgesRaw = dict()
moviesDict = dict()

# with open("Tsv\imdbCrew.tsv", encoding="utf-8") as tsv:
#     next(tsv)
#     for line in tsv:
#         sLine = line.split("\t")
#         crew[sLine[0]] = sLine
#
# with open("Tsv\ImdbBasics.tsv", encoding="utf-8") as tsv:
#     next(tsv)
#     for line in tsv:
#         sLine = line.split("\t")
#         if sLine[1] == "movie" and sLine[5] != "\\N" and sLine[8] != "\\N\n" and "1960" < sLine[5] < "1970" and sLine[4] != "1":
#             # if sLine[1] == "movie" and sLine[5] > "2015":
#             mov = movie(sLine)
#             movies.append(mov)
#             directors = crew[sLine[0]][1].split(",")
#             if directors != "\\N":
#                 for director in directors:
#                     if director in crewMember:
#                         crewMember[director].append(sLine[0])
#                     else:
#                         crewMember[director] = [sLine[0]]
#             writers = crew[sLine[0]][2].replace("\n", "").split(",")
#             if writers != "\\N":
#                 for writer in writers:
#                     if writer in crewMember:
#                         if crewMember[writer].count(sLine[0]) == 0:
#                             crewMember[writer].append(sLine[0])
#                     else:
#                         crewMember[writer] = [sLine[0]]


# with open("Tsv\imdbPrincipals.tsv", encoding="utf-8") as tsv:
#     next(tsv)
#     for line in tsv:
#         sLine = line.split("\t")
#         if sLine[0] in crew:
#             crew[sLine[0]].append(sLine[2])
#         else:
#             crew[sLine[0]] = [sLine[2]]

with open("Tsv\imdbCrew.tsv", encoding="utf-8") as tsv:
    next(tsv)
    for line in tsv:
        sLine = line.split("\t")
        crew[sLine[0]] = sLine

with open("Tsv\ImdbBasics.tsv", encoding="utf-8") as tsv:
    next(tsv)
    for line in tsv:
        sLine = line.split("\t")
        if sLine[5] != "\\N" and sLine[8] != "\\N\n" and "2000" <= sLine[5] < "2010":
            if sLine[0] in crew:  # if the movie has no social features it cant be predicted
                mov = movie(sLine)
                moviesRaw.append(mov)
                directors = crew[sLine[0]][1].split(",")
                if directors != "\\N":
                    for director in directors:
                        if director in crewMember:
                            crewMember[director].append(sLine[0])
                        else:
                            crewMember[director] = [sLine[0]]

crewMember["\\N"] = []  # works good enough but doesent remove the actual key
# print(crewMember["\\N"])
for member, value in crewMember.items():
    if len(value) > 1:
        for i in range(0, len(value), 1):
            for j in range(i + 1, len(value), 1):
                if value[i] in movieEdgesRaw:
                    movieEdgesRaw[value[i]].append(value[j])
                else:
                    movieEdgesRaw[value[i]] = [value[j]]


movies = []
movieEdges = dict()
moviesPrev = moviesRaw
movieEdgesPrev = movieEdgesRaw
for i in range(0, 1):
    movies = []
    movieEdges = dict()
    for movie in moviesPrev:
        if movie.id in movieEdgesPrev and len(movieEdgesPrev[movie.id]) > 5:
            movies.append(movie)
            movieEdges[movie.id] = movieEdgesPrev[movie.id]

    moviesDict = dict()
    for movie in movies:
        moviesDict[movie.id] = movie

    for id, edgeList in movieEdges.items():
        newList = []
        for movieId in edgeList:
            if movieId in moviesDict:
                newList.append(movieId)
        movieEdges[id] = newList
    print("removed {0} movies".format(len(moviesPrev) - len(movies)))
    moviesPrev = movies
    movieEdgesPrev = movieEdges

print("removed total {0} movies".format(len(moviesRaw) - len(movies)))

actualMovies = 0
for movie in movies:
    if movie.titleType == "movie":
        actualMovies += 1

genreCountTotal = Helper.genreCount(movies)

print(Helper.genreCount(movies))
print(genreCountTotal.keys())

print(datetime.now() - time)
# print(edge)
print("nr of edges: {0}".format(len(movieEdges)))
print("nr of movies: {0}".format(len(movies)))
print("nr of actual movies: {0}".format(actualMovies))
print("nr of crew: {0}".format(len(crew)))
print("nr of crew members: {0}".format(len(crewMember)))

moviesTrain = copy.deepcopy(movies)

for movie in moviesTrain:
    if random.random() > 0.20:
        movie.genres = []
        movie.markedAsUnknown = True

moviesDict = dict()
for movie in moviesTrain:
    moviesDict[movie.id] = movie

print(Helper.genreCount(moviesTrain))

# Algorithms.RNStar(moviesTrain, movieEdges, moviesDict, 5, False, 0.66)
# Algorithms.RNStar(moviesTrain, movieEdges, moviesDict, 5, True, 0.66)
# Algorithms.pRNStar(moviesTrain, movieEdges, moviesDict, list(genreCountTotal.keys()), 5, False, 0.10)
Algorithms.pRNStar(moviesTrain, movieEdges, moviesDict, list(genreCountTotal.keys()), 5, True, 0.10)



print(Helper.genreCount(moviesTrain))
countCorrect = 0
countUnknown = 0
countNoNeighbours = 0
countNotGuessed = 0
hammingLoss = 0.0
possibleGenres = list(genreCountTotal.keys())
possibleGenres.sort()
confusionMatrix = dict()

for genre in possibleGenres:  # 0:TP, 1:TN 2:FN, 3:FP, 4: R0(recall), 5: precision, 6: F
    confusionMatrix[genre] = [0, 0, 0, 0, 0, 0, 0]

for index, movie in enumerate(moviesTrain):
    if movie.markedAsUnknown:
        countUnknown += 1
        movie.genres.sort()
        movies[index].genres.sort()
        if not movie.genres:
            countNotGuessed += 1
        if movie.genres == movies[index].genres:
            countCorrect += 1
        if movie.id not in movieEdges:
            countNoNeighbours += 1
        for genre in possibleGenres:
            if (genre in movie.genres) != (genre in movies[index].genres):
                hammingLoss += 1 / len(possibleGenres)
            if genre in movie.genres:  # TP | FP
                if genre in movies[index].genres:  # TP
                    confusionMatrix[genre][0] += 1
                else:  # FP
                    confusionMatrix[genre][3] += 1
            else:  # TN | FN
                if genre in movies[index].genres:  # FN
                    confusionMatrix[genre][2] += 1
                else:  # TN
                    confusionMatrix[genre][1] += 1
avgF1 = 0.0
macroAvgR = 0.0
macroAvgP = 0.0
totalTP = 0
totalFP = 0
totalFN = 0
for genre in possibleGenres:
    totalTP += confusionMatrix[genre][0]
    totalFP += confusionMatrix[genre][3]
    totalFN += confusionMatrix[genre][2]

    if (confusionMatrix[genre][0] + confusionMatrix[genre][2]) != 0:
        confusionMatrix[genre][4] = confusionMatrix[genre][0] / (confusionMatrix[genre][0] + confusionMatrix[genre][2])
    macroAvgR += confusionMatrix[genre][4]

    if (confusionMatrix[genre][0] + confusionMatrix[genre][3]) != 0:
        confusionMatrix[genre][5] = confusionMatrix[genre][0] / (confusionMatrix[genre][0] + confusionMatrix[genre][3])
    macroAvgP += confusionMatrix[genre][5]

    if (confusionMatrix[genre][4] + confusionMatrix[genre][5]) != 0:
        confusionMatrix[genre][6] = (2 * confusionMatrix[genre][4] * confusionMatrix[genre][5]) / (
                confusionMatrix[genre][4] + confusionMatrix[genre][5])
    avgF1 += confusionMatrix[genre][6]
    print("{0}:{1}]".format(genre, confusionMatrix[genre]))

macroAvgR /= len(possibleGenres)
macroAvgP /= len(possibleGenres)
avgF1 /= len(possibleGenres)

microAvgR = totalTP / (totalTP + totalFN)
microAvgP = totalTP / (totalTP + totalFP)

print("accuracy {0}".format(countCorrect / countUnknown))
print("% no neighbour {0}".format(countNoNeighbours / countUnknown))
print("% not guessed {0}".format(countNotGuessed / countUnknown))

print("% hamming loss {0}".format(hammingLoss / countUnknown))

print("Macro Avg P {0}".format(macroAvgP))
print("Macro Avg R {0}".format(macroAvgR))
print("Macro F1 {0}".format(((2 * macroAvgR * macroAvgP) / (macroAvgR + macroAvgP))))

print("Micro Avg R {0}".format(microAvgR))
print("Micro Avg P {0}".format(microAvgP))
print("Micro F1 {0}".format(((2 * microAvgR * microAvgP) / (microAvgR + microAvgP))))

print(datetime.now() - time)
