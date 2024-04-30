from SPARQLWrapper import SPARQLWrapper, JSON

queryShortestPath = """
    PREFIX path: <http://www.ontotext.com/path#>
    PREFIX ex: <http://example.org/>

    SELECT ?pathIndex ?edgeIndex ?edge
    WHERE {
        VALUES (?src ?dst) {
            ( ex:UnsustainableEnergyUse ex:GlobalWarming )
        }
        SERVICE path:search {
            [] path:findPath path:shortestPath ;
            path:sourceNode ?src ;
            path:destinationNode ?dst ;
            path:pathIndex ?pathIndex ;
            path:resultBindingIndex ?edgeIndex ;
            path:resultBinding ?edge ;
            .
        }
    }
"""

queryNarrowMatch = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE { ?a rdfs:label ?label }
    LIMIT 10
                
PREFIX ex: <http://example.org/>

SELECT ?hasNarrowMatch
WHERE {
    OPTIONAL {ex:HumanActivities ex:cause ex:GlobalWarming}
    BIND (exists{ex:HumanActivities ex:cause ex:GlobalWarming} AS ?y)
	BIND (IF(?y, "true", "false") AS ?hasNarrowMatch)
} 
"""               


sparql = SPARQLWrapper("http://ct-Laptop:7200/repositories/LLM_unrefined")
sparql.setQuery(queryShortestPath)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print(results)
for result in results["results"]["bindings"]:
    print("pathIndex: " + result["pathIndex"]["value"])
    print("edgeIndex: " + result["edgeIndex"]["value"])

#print('---------------------------')
#print (results) # {'head': {'vars': ['label']}, 'results': {'bindings': [{'label': {'type': 'literal', 'value': 'Atlantic Meridional Overturning Circulation'}}]}}
""" for result in results["results"]["bindings"]:
    print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"])) """