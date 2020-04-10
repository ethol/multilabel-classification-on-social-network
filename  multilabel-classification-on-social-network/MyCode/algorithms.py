from lib import Helper

class Algorithms:
    @staticmethod
    def RNStar(moviesTrain, movieEdges, moviesDict, maxItr, threshold):
        previousCount = dict()
        for i in range(0, maxItr):
            print("{0}/{1}".format(i, maxItr))
            print(Helper.genreCount(moviesTrain))
            if previousCount == Helper.genreCount(moviesTrain):
                break
            previousCount = Helper.genreCount(moviesTrain)
            for index, movie in enumerate(moviesTrain):
                if movie.markedAsUnknown and movie.id in movieEdges:
                    genres = dict()
                    totalNeighbours = 0
                    for neighbourEdge in movieEdges[movie.id]:
                        neighbourMovie = moviesDict[neighbourEdge]
                        if neighbourMovie.genres:
                            totalNeighbours += 1
                            for genre in neighbourMovie.genres:
                                if genre in genres:
                                    genres[genre] += 1
                                else:
                                    genres[genre] = 1

                    movie.genres = []
                    for genre, number in genres.items():
                        if totalNeighbours != 0 and (number / totalNeighbours) >= threshold:
                            movie.genres.append(genre)

    @staticmethod
    def pRNStar(moviesTrain, movieEdges, moviesDict, possibleGenre, maxItr, threshold):

        #Initialize
        for index, movie in enumerate(moviesTrain):
            if movie.markedAsUnknown and movie.id in movieEdges:
                for genre in possibleGenre:
                    movie.probabilityEstimates[genre] = 0.0

        for i in range(0, maxItr):
            print("{0}/{1}".format(i, maxItr))
            for index, movie in enumerate(moviesTrain):
                if movie.markedAsUnknown and movie.id in movieEdges:
                    genres = dict()
                    for neighbourEdge in movieEdges[movie.id]:
                        neighbourMovie = moviesDict[neighbourEdge]
                        if neighbourMovie.markedAsUnknown:
                            for genre in possibleGenre:
                                if genre in genres:
                                    genres[genre] += neighbourMovie.probabilityEstimates[genre]
                                else:
                                    genres[genre] = neighbourMovie.probabilityEstimates[genre]
                        else:
                            for genre in neighbourMovie.genres:
                                if genre in genres:
                                    genres[genre] += 1.0
                                else:
                                    genres[genre] = 1.0


                    for genre, number in genres.items():
                        movie.probabilityEstimates[genre] = number / len(movieEdges[movie.id])

        for index, movie in enumerate(moviesTrain):
            if movie.markedAsUnknown:
                movie.genres = []
                for genre in possibleGenre:
                    if movie.probabilityEstimates[genre] > threshold:
                        movie.genres.append(genre)

