from numpy import dot
from numpy.linalg import norm

def cosineSimilarity(a, b):
    return dot(a, b)/(norm(a)*norm(b))


def calculatingTripleScore(veracity, extractedTriple):
    print("calculating triple score")
    clearness = 1
    confidence = 1
    if veracity == "true":
        veracityScore = 1
    else:
        veracityScore = 0
    tripleScore = (veracityScore+clearness+confidence)/3
    return veracityScore



