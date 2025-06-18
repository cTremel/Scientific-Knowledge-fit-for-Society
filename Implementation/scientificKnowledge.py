from processMedia import processMedia, loadProcessedMedia
from extractTriples import extractTriples
from extendKnowledgeGraph import extendingKnowledgeGraph
from checkVeracity import checkingVeracity
from calculateTripleScore import calculatingTripleScore
from calculateMediaScore import calculatingMediaScore
import os

ipcc = {"fileLocation": "0_media/trusted/AR6 Synthesis Report_ Summary for Policymakers Headline Statements.pdf", "fileType": "pdf", "downloadUrl": "https://www.ipcc.ch/report/ar6/syr/resources/spm-headline-statements/", "accessDate": ""}
# processMedia(ipcc)

article = {"fileLocation": "0_media/The Effects of Climate Change.txt", "fileType": "web", "downloadUrl": "https://science.nasa.gov/climate-change/effects/", "accessDate": ""}
# processMedia(article)

audio = {"fileLocation": "0_media/Climate change explained in under 2 minutes.mp3", "fileType": "audio", "downloadUrl": "", "accessDate": ""}
#processMedia(audio)

folder = ""
filetype = "audio"
# for file in os.listdir("0_media/" + folder):
#     if file.endswith(".mp3"):
#         media = {"fileLocation": "0_media/" + folder + "/" + file, "fileType": filetype, "downloadUrl": "", "accessDate": ""}
#         processMedia(media)

# processedMedia = loadProcessedMedia(article)

# text = processedMedia["text"]
# triples = extractTriples(text)

extractedTrustedTriples = ""
extendingKnowledgeGraph(extractedTrustedTriples)

trustedMediaSources = [ipcc["fileLocation"]]


#extractedMediaTriples = [{"subject": "ex:HumanActivities", "predicate": "ex:cause", "object": "ex:GlobalWarming", "sourceMedia": [0]}]
knowledgeGraph = "http://ct-Laptop:7200/repositories/LLM_unrefined"


processedMedia = loadProcessedMedia(article)
extractedMediaTriples = extractTriples(processedMedia["text"])
if extractedMediaTriples == "No Answer":
    print("No Answer")
    #extractedMediaTriples = loadTriples(processedMedia)
    extractedMediaTriples = [{"subject": "ex:HumanActivities", "predicate": "ex:cause", "object": "ex:GlobalWarming", "sourceMedia": [0]}]

counter = 0
tripleScores = []
for triple in extractedMediaTriples:
    counter = counter + 1
    print("Statement {}".format(counter))
    veracity = checkingVeracity(triple, knowledgeGraph)
    tripleScore = calculatingTripleScore(veracity, triple)
    tripleScores.append(tripleScore)
    

mediaScore = calculatingMediaScore(tripleScores)

print("{} has a media score of {} from possible {}.".format(processedMedia["title"], mediaScore, counter))
