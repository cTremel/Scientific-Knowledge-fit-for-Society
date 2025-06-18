import spacy
import amrlib
import penman
import json
from typing import TypedDict

from rapidfuzz.distance import Levenshtein
from nltk.corpus import wordnet as wn
from nltk import WordNetLemmatizer

amrlib.setup_spacy_extension()
nlp = spacy.load('en_core_web_sm')
text = 'Severe weather damage will also increase and intensify.'

doc = nlp(text)
print(len(doc.sents))
#graphs = doc._.to_amr()

""" processedMedia = dict()
class extractedTriple(TypedDict):
    sentenceNumber: int
    processedSentence: str
    triples: tuple(str) """

# print(graphs)
# with open("span.txt", "w") as outfile:
#     for span in doc.sents:
#         graphs = span._.to_amr()
#         print(graphs[0])
#         outfile.write(graphs[0])


""" i = 0
with open("amr.json", "w") as outfile:
    for graph in graphs:
        i = i + 1
        eT= dict(sentenceNumber=i, processedSentence="", triples=[graph])
        outfile.write(eT) """

""" with open("graphs.json", "w") as outfile:
    for graph in graphs:
        outfile.write(graph) """
    
""" # Opening JSON file
with open('amr.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)
 
print(json_object)
print(type(json_object)) """

#Declare some necessary global functions and objects
stog = amrlib.load_stog_model()
wordnet_lemmatizer = WordNetLemmatizer()
#stop_words = set(stopwords.words('english'))
#current_time_ms = lambda: int(round(time.time() * 1000))

def amr_triplets(g, nps):
    '''
    inputs:
        - g: AMR graph
        - nps: a list of noun phrases (extracted using a syntactic parser)
    outputs:
        - triplets (subject, object, relation)
    '''
    
    triplets = []
    entities = {}
    gg = penman.decode(g)
    
    #Map the variables to their corresponding lexicons
    for (src, role, target) in gg.instances():
        entities[src] = target
        
    D = {}
    #Find a node that relates to the input subject (e1)
    for (src, role, target) in gg.edges():
        if src in D.keys():
            D[src][role] = target
        else:
            D[src] = {}
            D[src][role] = target
    
    #print(g)
    #print(entities)
    #print(D)
    
           
    for src in D.keys():
        
        '''
        :name
        process specification
        '''
        src_alias = None
        if ":name" in D[src].keys():
            src_alias = D[src][":name"]
        '''
        Process ARG semantic type
        ''' 
        if ":ARG0" in D[src].keys() and ":ARG1" in D[src].keys():
            
            sub = show_entry(D, entities, D[src][":ARG0"])
            
            obj = show_entry(D, entities, D[src][":ARG1"])
            if src_alias is None:
                rel = entities[src]
            else:
                rel = entities[src_alias]
                        
            triplets.append(fix_tuple(sub,obj,rel,nps))
            
        #elif ":ARG1" in D[src].keys() and ":ARG2" in D[src].keys():
            
            #sub = show_entry(D, entities, D[src][":ARG1"])
            #obj = show_entry(D, entities, D[src][":ARG2"])
            #rel = show_entry(D, entities, src)
                        
            #triplets.append(fix_tuple(sub,obj,rel,nps))
        
        '''
        :ARG1-of / cause-01
        penman handles "/d :ARG1-of /c cause-01" as ":ARG0 :ARG1" pattern
        '''
        #if ":ARG1-of" in D[src].keys() and entities[D[src][":ARG1-of"]]=="cause-01":
        #    print(("*"*5)+"CAUSE role"+("*"*5))
        #    print(entities)
        #    print(D[src])
        
        '''
        :consist-of
        panman reverses any -of role in AMR. "A :consist-of B" becomes "B :consist A"
        '''
        if ":consist" in D[src].keys():
            
            sub = show_entry(D, entities, D[src][":consist"])
            
            if src_alias is None:
                obj = show_entry(D, entities, src)
            else:
                obj = show_entry(D, entities, src_alias)
            rel = "contains"
            
            triplets.append(fix_tuple(sub,obj,rel,nps))
            
        
                
    return triplets

def show_entry(D, entities, src):
    '''
    Inputs:
        D: Semantic parse tree in a json (dictionary format)
        entities: variable-lexicon mapping for the parse tree entries
        src: a variable in the parse tree
        
    Output:
        string -- the appropriate lexicon for the "src" variable
    '''
    entity_base_str = entities[src]
    if "-0" in entity_base_str:
        entity_base_str = entity_base_str[0:entity_base_str.find("-0")]
        
    entity_str = ""
    
    if src in D.keys():
        #Process conjunction (and/or)
        if ((entity_base_str=="and") or (entity_base_str=="or")):
            options = [op for op in D[src].keys() if ":op" in op]
            
            if len(options)!=0:
                entity_str = show_entry(D,entities,D[src][options[0]])
                for op in options[1:]:
                    entity_str+=" "+entity_base_str+" "
                    entity_str+=convert(show_entry(D,entities,D[src][op]))
                    
        elif (entity_base_str=="name"):
            options = [op for op in D[src].keys() if ":op" in op]
            
            if len(options)!=0:
                entity_str = show_entry(D,entities,D[src][options[0]])
                for op in options[1:]:
                    entity_str+=" "
                    entity_str+=show_entry(D,entities,D[src][op])    
                
            
        #Process :mod relation
        elif ":mod" in D[src].keys():  
            entity_str = convert(entity_base_str)
            if D[src][":mod"] in D.keys() and ":mod" in D[D[src][":mod"]].keys():
                entity_str =entities[D[D[src][":mod"]][":mod"]]+" "+entity_str
            else:
                entity_str = entities[D[src][":mod"]]+" "+entity_str
    
        else:
            entity_str = convert(entity_base_str)
    else:
        entity_str = convert(entity_base_str)
    #entity_str += entities[src]
    #print(entity_base_str, entity_str)
    #print(entity_base_str)
    return entity_str

def fix_tuple(sub,obj,rel,nps):
    '''
    Final level modification to a (subject, object, relation) tuple
    Inputs:
        (sub,obj,rel): triplet obtained from semantic parser
        nps: noun phrases obtained from a syntactic parse
        
    Outputs:
        (sub,obj,rel): remove AMR specific codecs and convert subject and object to its noun form (whenever possible)
    '''
    
    #discard AMR specific tags (cause-01 -> cause)
    if "-0" in sub:
        sub = sub[0:sub.find("-0")]

    if "-0" in obj:
        obj = obj[0:obj.find("-0")]

    if "-0" in rel:
        rel = rel[0:rel.find("-0")]
        

    sub_nps = []
    obj_nps = []
    for np in nps:
        #If subject or object matches the postfix of any of the noun phrases, that noun phrase becomes the new subject/object
        if wordnet_lemmatizer.lemmatize(np.split(" ")[-1].lower()) == wordnet_lemmatizer.lemmatize(sub.lower()):
            sub_nps.append(np)

        if wordnet_lemmatizer.lemmatize(np.split(" ")[-1].lower()) == wordnet_lemmatizer.lemmatize(obj.lower()):
            obj_nps.append(np)

    '''
    Subject and object should be nouns
    '''
    sub = convert(sub)
    obj = convert(obj)
    
    if len(sub_nps)==1:
        sub = sub_nps[0]

    if len(obj_nps)==1:
        obj = obj_nps[0]

        
    return (sub,obj,rel)

def convert(word, from_pos="v", to_pos="n"):    
    """ 
        Transform words given from/to POS tags.
        The assumption is, in a (subject, object, verb) triplet, subject and object should be noun-phrases
    """
    
    WN_NOUN = 'n'
    WN_VERB = 'v'
    WN_ADJECTIVE = 'a'
    WN_ADJECTIVE_SATELLITE = 's'
    WN_ADVERB = 'r'

    # If the word is already in desired form, no need to modify
    synsets = wn.synsets(word, pos=to_pos)
    if synsets:
        return word
    
    synsets = wn.synsets(word, pos=from_pos)

    # Word not found, perhaps the word is not a verb, and maybe already a noun
    if not synsets:
        return word

    # Get all lemmas of the word (consider 'a'and 's' equivalent)
    lemmas = []
    for s in synsets:
        for l in s.lemmas():
            if s.name().split('.')[1] == from_pos or from_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and s.name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                lemmas += [l]

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]

    # filter only the desired pos (consider 'a' and 's' equivalent)
    related_noun_lemmas = []

    for drf in derivationally_related_forms:
        for l in drf[1]:
            if l.synset().name().split('.')[1] == to_pos or to_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and l.synset().name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                related_noun_lemmas += [l]

    # Extract the words from the lemmas
    words = [l.name() for l in related_noun_lemmas]
    len_words = len(words)

    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w)) / len_words) for w in set(words)]
    result.sort(key=lambda w:-w[1])
    
    #Get the noun that is closer to the word syntactically (edit distance) and matches symantically
    d = 10000
    i = 0
    res = ""
    for entry in result:
        '''
        when converting from verb to noun, insertion is natural
        entry[1] is the probability/semantic similarity, so (1-entry[1]) can be a distance
        '''
        edit_distance = (1-entry[1])*Levenshtein.distance(word,entry[0],weights=(0.5,1,1))
        if d>edit_distance:
            d = edit_distance
            res = entry[0]
        if i==3:
            break

    # return all the possibilities sorted by probability
    return res

""" pgraph = penman.load('text.txt')
print(len(pgraph))
for graph in pgraph:
    print("\n penman" + pgraph)
 """