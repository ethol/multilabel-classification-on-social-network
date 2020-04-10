class movie:
    id = ""
    titleType = ""
    primaryTitle = ""
    originalTitle = ""
    year = None
    runTime = None
    genres = []
    markedAsUnknown = False
    probabilityEstimates = dict()
    
    def __init__(self, list):
        self.id = list[0]
        self.titleType = list[1]
        self.primaryTitle = list[2]
        self.originalTitle = list[3]
        self.year = None if list[5] == "\\N" else int(list[5])
        self.runTime = None if list[7] == "\\N" else int(list[7])
        self.genres = list[8].replace("\n", "").split(",")
        self.probabilityEstimates = dict()

    def toString(self):
        print(self.year)
