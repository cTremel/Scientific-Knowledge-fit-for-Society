import spacy
import os
import json

IPCC_keywords = ['human activities', 'emissions', 'greenhouse gas', 'CO2', 'climate change', 'global warming', 'weather', 'adaptation', 'implementation', 'action', 'mitigation', 'policies', 'laws', 'climate goals', 'risks', 'impacts', 'losses', 'damages']

def write_list(a_list, file):
    with open(file, "w") as fp:
        json.dump(a_list, fp)

# Read list to memory
def read_list(file):
    # for reading also binary mode is important
    with open(file, 'rb') as fp:
        n_list = json.load(fp)
        return n_list

nlp = spacy.load('en_core_web_sm')

directory = 'Test'
output_directory = directory + '/reduced'
keyword_file = 'keywords/IPCC.txt'

if not os.path.isdir(output_directory):
    os.mkdir(output_directory)

#write_list(IPCC_keywords, keyword_file)
domain_specific_keywords = read_list(keyword_file)

for filename in os.listdir(directory):
    if filename == 'prompt.txt':
        continue
    if filename.endswith('.txt'):
        with open(os.path.join(directory, filename)) as f:
            text = f.read()
        doc = nlp(text)
        result = ""
        for sentence in doc.sents:
            #print(sentence)
            for keyword in domain_specific_keywords:
                #print(keyword)
                if keyword in sentence.text:
                    result += sentence.text
                    break
        output = open(os.path.join(output_directory, filename),'w')
        output.write(result)





