from helpers import cleaning
import numpy as np

def edge_tuple_creation(text):
    
    initial_tup_ls = cleaning.create_svo_triples(text)
    init_obj_tup_ls = cleaning.get_obj_properties(initial_tup_ls)
    new_layer_ls = cleaning.add_layer(init_obj_tup_ls)
    starter_edge_ls = init_obj_tup_ls + new_layer_ls
    edge_ls = cleaning.subj_equals_obj(starter_edge_ls)
    edges_word_vec_ls = cleaning.create_word_vectors(edge_ls)
    
    return edges_word_vec_ls


def node_tuple_creation(edges_word_vec_ls):
    
    orig_node_tup_ls = [(edges_word_vec_ls[0][0], '', ['Subject'], '', np.random.uniform(low=-1.0, high=1.0, size=(300,)))]
    obj_node_tup_ls = [(tup[2], tup[3], tup[4], tup[5], tup[6]) for tup in edges_word_vec_ls]
    full_node_tup_ls = orig_node_tup_ls + obj_node_tup_ls
    cleaned_node_tup_ls = cleaning.check_for_string_labels(full_node_tup_ls)
    #dedup_node_tup_ls = dedup(cleaned_node_tup_ls)
    dedup_node_tup_ls = cleaned_node_tup_ls
    node_tup_ls = convert_vec_to_ls(dedup_node_tup_ls)
    
    return node_tup_ls    


def dedup(tup_ls):
    
    visited = set()
    output_ls = []
    
    for tup in tup_ls:
        if not tup[0] in visited:
            visited.add(tup[0])
            output_ls.append((tup[0], tup[1], tup[2], tup[3], tup[4]))
            
    return output_ls

def convert_vec_to_ls(tup_ls):
    
    vec_to_ls_tup = []
    
    for el in tup_ls:
        vec_ls = [float(v) for v in el[4]]
        tup = (el[0], el[1], el[2], el[3], vec_ls)
        vec_to_ls_tup.append(tup)
        
    return vec_to_ls_tup

# does not work without py2neo
""" def add_nodes(tup_ls):   

    keys = ['name', 'description', 'node_labels', 'url', 'word_vec']
    merge_nodes(graph.auto(), tup_ls, ('Node', 'name'), keys=keys)
    print('Number of nodes in graph: ', graph.nodes.match('Node').count())
    
    return """
    
    
    
""" def add_edges(edge_ls):
    
    edge_dc = {} 
    
    # Group tuple by verb
    # Result: {verb1: [(sub1, v1, obj1), (sub2, v2, obj2), ...],
    #          verb2: [(sub3, v3, obj3), (sub4, v4, obj4), ...]}
    
    for tup in edge_ls: 
        if tup[1] in edge_dc: 
            edge_dc[tup[1]].append((tup[0], tup[1], tup[2])) 
        else: 
            edge_dc[tup[1]] = [(tup[0], tup[1], tup[2])] 
    
    for edge_labels, tup_ls in tqdm(edge_dc.items()):   # k=edge labels, v = list of tuples
        
        tx = graph.begin()
        
        for el in tup_ls:
            source_node = nodes_matcher.match(name=el[0]).first()
            target_node = nodes_matcher.match(name=el[2]).first()
            if not source_node:
                source_node = Node('Node', name=el[0])
                tx.create(source_node)
            if not target_node:
                try:
                    target_node = Node('Node', name=el[2], node_labels=el[4], url=el[5], word_vec=el[6])
                    tx.create(target_node)
                except:
                    continue
            try:
                rel = Relationship(source_node, edge_labels, target_node)
            except:
                continue
            tx.create(rel)
        tx.commit()
    
    return """