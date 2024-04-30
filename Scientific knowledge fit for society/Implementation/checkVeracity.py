from SPARQLWrapper import SPARQLWrapper, JSON



def checkForNarrowMatch(triple, knowledgeGraphUrl):
    if type(triple) == dict:
        subject = triple["subject"]
        predicate = triple["predicate"]
        object = triple["object"]
    elif type(triple) == list and len(triple) == 3:
        subject = triple[0]
        predicate = triple[1]
        object = triple[2]

    triple = "{} {} {}".format(subject, predicate, object)

    queryNarrowMatch = "PREFIX ex: <http://example.org/> PREFIX : <http://example.net/> SELECT ?hasNarrowMatch WHERE {OPTIONAL {"+triple+"} BIND (exists{"+triple+"} AS ?y) BIND (IF(?y, 'true', 'false') AS ?hasNarrowMatch) }"

    sparql = SPARQLWrapper(knowledgeGraphUrl)
    sparql.setQuery(queryNarrowMatch)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    bindings = results["results"]["bindings"]
    value = bindings[0]["hasNarrowMatch"]["value"]
    return value

def getShortestPath(triple, knowledgeGraphUrl):
    if type(triple) == dict:
        subject = triple["subject"]
        predicate = triple["predicate"]
        object = triple["object"]
    elif type(triple) == list and len(triple) == 3:
        subject = triple[0]
        predicate = triple[1]
        object = triple[2]

    borders = "{} {}".format(subject, object)

    queryShortestPath = "PREFIX path: <http://www.ontotext.com/path#> PREFIX ex: <http://example.org/> SELECT ?pathIndex ?edgeIndex ?edge WHERE {VALUES (?src ?dst) {("+borders+")} SERVICE path:search { [] path:findPath path:shortestPath ;path:sourceNode ?src ; path:destinationNode ?dst ;path:pathIndex ?pathIndex ; path:resultBindingIndex ?edgeIndex ; path:resultBinding ?edge ; . } }"

    sparql = SPARQLWrapper(knowledgeGraphUrl)
    sparql.setQuery(queryShortestPath)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results



def checkingVeracity(triple, knowledgeGraphUrl):
    print("checking veracity")
    
    veracityScore = checkForNarrowMatch(triple, knowledgeGraphUrl)
    if veracityScore == "true":
        print("{} was matched in the KG".format(triple))
    return veracityScore