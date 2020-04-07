class Helper:
    @staticmethod
    def genreCount(movies):
        genresCount = dict()
        for movie in movies:
            for genre in movie.genres:
                if genre in genresCount:
                    genresCount[genre] += 1
                else:
                    genresCount[genre] = 1
        return genresCount