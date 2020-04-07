from lib import Helper

class Algorithms:
    @staticmethod
    def RNStar(moviesTrain, movieEdges, moviesDict):
        previousCount = dict()
        maxItr = 100
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
                        if totalNeighbours != 0 and number / totalNeighbours >= 0.75:
                            movie.genres.append(genre)