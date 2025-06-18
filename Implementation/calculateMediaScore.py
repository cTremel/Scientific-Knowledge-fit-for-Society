def calculatingMediaScore(tripleScores):
    print("calculating media score")
    if(len(tripleScores) == 0):
        print("no triple scores")
        return -1
    mediaScore = sum(tripleScores)/len(tripleScores)
    return sum(tripleScores)