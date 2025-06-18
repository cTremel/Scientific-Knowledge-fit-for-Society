import re
import spacy
import json
import urllib.parse, urllib.request
import numpy as np

SUBJECTS = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
VERBS = ['ROOT', 'advcl']
OBJECTS = ["dobj", "dative", "attr", "oprd", 'pobj']
ENTITY_LABELS = ['PERSON', 'NORP', 'GPE', 'ORG', 'FAC', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART']

non_nc = spacy.load('en_core_web_lg')

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('merge_noun_chunks')

def remove_special_characters(text):
    
    regex = re.compile(r'[\n\r\t]')
    clean_text = regex.sub(" ", text)
    
    return clean_text


def remove_stop_words_and_punct(text, print_text=False):
    
    result_ls = []
    rsw_doc = non_nc(text)
    
    for token in rsw_doc:
        if print_text:
            print(token, token.is_stop)
            print('--------------')
        if not token.is_stop and not token.is_punct:
            result_ls.append(str(token))
    
    result_str = ' '.join(result_ls)

    return result_str

def create_svo_lists(doc, print_lists):
    
    subject_ls = []
    verb_ls = []
    object_ls = []

    for token in doc:
        if token.dep_ in SUBJECTS:
            subject_ls.append((token.lower_, token.idx))
        elif token.dep_ in VERBS:
            verb_ls.append((token.lemma_, token.idx))
        elif token.dep_ in OBJECTS:
            object_ls.append((token.lower_, token.idx))

    if print_lists:
        print('SUBJECTS: ', subject_ls)
        print('VERBS: ', verb_ls)
        print('OBJECTS: ', object_ls)
    
    return subject_ls, verb_ls, object_ls

def remove_duplicates(tup, tup_posn):
    
    check_val = set()
    result = []
    
    for i in tup:
        if i[tup_posn] not in check_val:
            result.append(i)
            check_val.add(i[tup_posn])
            
    return result

def remove_dates(tup_ls):
    
    clean_tup_ls = []
    for entry in tup_ls:
        if not entry[2].isdigit():
            clean_tup_ls.append(entry)
    return clean_tup_ls


def create_svo_triples(text, print_lists=False):
    
    clean_text = remove_special_characters(text)
    doc = nlp(clean_text)
    subject_ls, verb_ls, object_ls = create_svo_lists(doc, print_lists=print_lists)
    
    graph_tup_ls = []
    dedup_tup_ls = []
    clean_tup_ls = []
    
    for subj in subject_ls: 
        for obj in object_ls:
            
            dist_ls = []
            
            for v in verb_ls:
                
                # Assemble a list of distances between each object and each verb
                dist_ls.append(abs(obj[1] - v[1]))
                
            # Get the index of the verb with the smallest distance to the object 
            # and return that verb
            index_min = min(range(len(dist_ls)), key=dist_ls.__getitem__)
            
            # Remve stop words from subjects and object.  Note that we do this a bit
            # later down in the process to allow for proper sentence recognition.

            no_sw_subj = remove_stop_words_and_punct(subj[0])
            no_sw_obj = remove_stop_words_and_punct(obj[0])
            
            # Add entries to the graph iff neither subject nor object is blank
            if no_sw_subj and no_sw_obj:
                tup = (no_sw_subj, verb_ls[index_min][0], no_sw_obj)
                graph_tup_ls.append(tup)
        
        #clean_tup_ls = remove_dates(graph_tup_ls)
    
    dedup_tup_ls = remove_duplicates(graph_tup_ls, 2)
    clean_tup_ls = remove_dates(dedup_tup_ls)
    
    return clean_tup_ls

api_key = open("/home/ct/Documents/Masterarbeit/Scripts/Knowledge Graph/helpers/.api_key").read()

def query_google(query, api_key, limit=10, indent=True, return_lists=True):
    
    text_ls = []
    node_label_ls = []
    url_ls = []
    
    params = {
        'query': query,
        'limit': limit,
        'indent': indent,
        'key': api_key,
    }   
    
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    url = service_url + '?' + urllib.parse.urlencode(params)
    response = json.loads(urllib.request.urlopen(url).read())
    
    if return_lists:
        for element in response['itemListElement']:

            try:
                node_label_ls.append(element['result']['@type'])
            except:
                node_label_ls.append('')

            try:
                text_ls.append(element['result']['detailedDescription']['articleBody'])
            except:
                text_ls.append('')
                
            try:
                url_ls.append(element['result']['detailedDescription']['url'])
            except:
                url_ls.append('')
                
        return text_ls, node_label_ls, url_ls
    
    else:
        return response

def get_obj_properties(tup_ls):
    
    init_obj_tup_ls = []
    
    for tup in tup_ls:

        try:
            text, node_label_ls, url = query_google(tup[2], api_key, limit=1)
            new_tup = (tup[0], tup[1], tup[2], text[0], node_label_ls[0], url[0])
        except:
            new_tup = (tup[0], tup[1], tup[2], [], [], [])
        
        init_obj_tup_ls.append(new_tup)
        
    return init_obj_tup_ls


def add_layer(tup_ls):

    svo_tup_ls = []
    
    for tup in tup_ls:
        
        if tup[3]:
            svo_tup = create_svo_triples(tup[3])
            svo_tup_ls.extend(svo_tup)
        else:
            continue
    
    return get_obj_properties(svo_tup_ls)
        

def subj_equals_obj(tup_ls):
    
    new_tup_ls = []
    
    for tup in tup_ls:
        if tup[0] != tup[2]:
            new_tup_ls.append((tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
            
    return new_tup_ls


def check_for_string_labels(tup_ls):
    # This is for an edge case where the object does not get fully populated
    # resulting in the node labels being assigned to string instead of list.
    # This may not be strictly necessary and the lines using it are commnted out
    # below.  Run this function if you come across this case.
    
    clean_tup_ls = []
    
    for el in tup_ls:
        if isinstance(el[2], list):
            clean_tup_ls.append(el)
            
    return clean_tup_ls


def create_word_vectors(tup_ls):

    new_tup_ls = []
    
    for tup in tup_ls:
        if tup[3]:
            doc = nlp(tup[3])
            new_tup = (tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], doc.vector)
        else:
            new_tup = (tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], np.random.uniform(low=-1.0, high=1.0, size=(300,)))
        new_tup_ls.append(new_tup)
        
    return new_tup_ls