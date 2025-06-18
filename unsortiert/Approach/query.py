from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://ct-Laptop:7200/repositories/ClimateSystemOntology")
sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE { ?a rdfs:label ?label }
    LIMIT 10
"""
# PREFIX ex: <http://example.org/>

# SELECT ?hasNarrowMatch
# WHERE {
#     OPTIONAL {ex:HumanActivities ex:cause ex:GlobalWarming}
#     BIND (exists{ex:HumanActivities ex:cause ex:GlobalWarming} AS ?y)
# 	BIND (IF(?y, "true", "false") AS ?hasNarrowMatch)
# }                
                )
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["label"]["value"])

#print('---------------------------')
#print (results) # {'head': {'vars': ['label']}, 'results': {'bindings': [{'label': {'type': 'literal', 'value': 'Atlantic Meridional Overturning Circulation'}}]}}
""" for result in results["results"]["bindings"]:
    print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"])) """