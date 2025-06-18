import openai
from transformers import AutoTokenizer
import torch
from transformers import pipeline
import spacy
import amrlib
from pathlib import Path
import json
from re import sub



def createAMRGraph(text):
    amrlib.setup_spacy_extension()
    nlp = spacy.load('en_core_web_sm')
    text = 'Severe weather damage will also increase and intensify.'

    doc = nlp(text)
    #print(len(doc.sents))
    graphs = doc._.to_amr()
    return graphs

def extractTriplesFromAMRGraph(graph):
    print("extracting triples from AMR Graph needs to be implemented")
    return ""


# # Set up your OpenAI API key
api_key = "YOUR_OPENAI_API_KEY"
openai.api_key = api_key

def generate_text(prompt):
# Call the OpenAI API to generate text based on the prompt
    response = openai.Completion.create(
        engine="text-davinci-002", # You can choose a different engine if needed
        prompt=prompt,
        max_tokens=100 # You can adjust this to control the length of the generated text
    )

    # Extract the generated text from the API response
    generated_text = response.choices[0].text.strip()
    return generated_text

def get_llama_response(prompt: str) -> str:

    model = "meta-llama/Llama-2-7b-chat-hf" # meta-llama/Llama-2-7b-hf

    tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token=True)

    llama_pipeline = pipeline(
        "text-generation",  # LLM task
        model=model,
        torch_dtype=torch.float32,
        device_map="auto",
    )

    """
    Generate a response from the Llama model.

    Parameters:
        prompt (str): The user's input/question for the model.

    Returns:
        None: Prints the model's response.
    """
    sequences = llama_pipeline(
        prompt,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=350,
    )
    return sequences[0]['generated_text']

def reduceText(text, keywords):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    result = ""
    for sentence in doc.sents:
        for keyword in keywords:
            if keyword in sentence.text:
                result += sentence.text
                break
    return result

# when format = True create an prompt that asks for .ttl format
def createPrompt(text, format=False):
    vocab = ["human activity", "emission", "greenhouse gas", "CO2", "climate change", "global warming", "adaptation", "implementation", "action", "mitigation", "policies", "policy", "law", "climate goal", "risk", "impact", "loss", "damage"]
    text = reduceText(text, vocab)
    if format:
        prompt = "You will perform the open information extraction task. You will identify the named entities in the content and then extract the relations between them. Based on the provided testimony, you will return triples, which are formatted as [named entity A, relation, named entity B]. START of the testimony:{}END of the testimony. The extracted triples formatted as .ttl are:".format(text)
    else:
        prompt = "You will perform the open information extraction task. You will identify the named entities in the content and then extract the relations between them. Based on the provided testimony, you will return triples, which are formatted as [named entity A, relation, named entity B]. Entities should not be more than 2 words. START of the testimony:{}END of the testimony. The extracted triples formatted as [named entity A, relation, named entity B] are:".format(text)
    return prompt


def getAnswer(prompt, method):
    if method == "gpt":
        if api_key == "YOUR_OPENAI_API_KEY":
            print("The API key is not setup. Please use a different model or setup the API key")
            result = "No Answer"
        else:
            result = generate_text(prompt)
    elif method == "llama":
        result = get_llama_response(prompt)
    elif method == "amr":
        graph = createAMRGraph()
        result = extractTriplesFromAMRGraph(graph)
    return result

def loadMediaTriples(location):

    return []

def identifyTriples(text, method):
    print("identifying triples")
    if method != "amr":
        input = createPrompt(text)
    else:
        input = text
    triples = getAnswer(input, method)
    return triples

# Define a function to convert a string to camel case
def camelCase(s):
    # Use regular expression substitution to replace underscores and hyphens with spaces,
    # then title case the string (capitalize the first letter of each word), and remove spaces
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    
    # Join the string, ensuring the first letter is lowercase
    return ''.join([s[0].lower(), s[1:]])

def baseVerbs(text, llm):
    basePrompt = "Please change the verbs of the following triples into their base form:{} The triples with verbs changed into their base form formatted as [named entity A, relation, named entity B] are:".format(text)

    triplesWithBasedVerbs = getAnswer(basePrompt, llm)
    if triplesWithBasedVerbs == "No Answer":
        triplesWithBasedVerbs = [["Climate Change", "encompass", "Global warming"],["Global warming", "refer to", "long-term warming"], ["Global warming", "encompass", "Climate change"], ["Humans", "cause", "major climate changes"], ["Humans", "emit", "greenhouse gases"],["Greenhouse gases","contribute to", "Global warming"], ["Global warming", "cause", "long-term warming"], ["Global warming", "cause", "rise in global temperatures"], ["Global warming", "cause", "flatten within a few years"]]
    return triplesWithBasedVerbs

def getSynonyms(text, llm, vocab):
    synonymPrompt = "Please write down all synonyms from list A and list B. Do not match different word types like nouns and verbs. Start of list A {} End of List A. Start of List B {} End of List B. The synonyms with no duplicates listed as pairs in the form of [synonym 1, synonym 2] with synonym 1 always unique are:".format(text, vocab)

    synonyms = getAnswer(synonymPrompt, llm)
    if synonyms == "No Answer":
        synonyms = [["Climate Change", "Climate change"],
                    ["Global warming", "globalWarming"],
                    ["encompass", "encompass"],
                    ["refer to", "refer to"],
                    ["long-term warming", "long-term warming"],
                    ["Humans", "humanActivity"],
                    ["cause", "cause"],
                    ["major climate changes", "climateChange"],
                    ["emit", "emit"],
                    ["greenhouse gases", "greenhouseGas"],
                    ["contribute to", "contributeTo"],
                    ["rise in global temperatures", "hasLevel"]]
    return synonyms

def alignTriples(text, llm):
    triplesWithBasedVerbs = baseVerbs(text, llm)

    vocab = ["humanActivity", "emission", "greenhouseGas", "CO2", "climateChange", "globalWarming", "adaptation", "implementation", "action", "mitigation", "policies", "policy", "law", "climateGoal", "risk", "impact", "loss", "damage", "cause", "emit", "reach", "contributeTo", "affect", "hasLevel"]
    vocabName = "ex:"
    
    synonyms = getSynonyms(triplesWithBasedVerbs,llm, vocab)
    triplesWithBaseVerbsAndCamelCaseAndVocabName = []
    for triple in triplesWithBasedVerbs:
        camelCaseTriple = []
        for string in triple:
            for synonym in synonyms:
                if string == synonym[0]:
                    string = synonym[1]
            if " " in string:
                camelCaseVocabString = camelCase(string)
            else:
                camelCaseVocabString = string
            if camelCaseVocabString in vocab:
                camelCaseVocabString = vocabName + camelCaseVocabString
            else:
                camelCaseVocabString = ":" + camelCaseVocabString
            camelCaseTriple.append(camelCaseVocabString)
        triplesWithBaseVerbsAndCamelCaseAndVocabName.append(camelCaseTriple)
    print("aligning triples")    
    return triplesWithBaseVerbsAndCamelCaseAndVocabName

#input media, output processedMedia 
def extractTriples(text):
    method = "gpt"
    candidateTriples = identifyTriples(text,method)
    if candidateTriples == "No Answer":
        candidateTriples = [["Climate Change", "encompasses", "Global warming"],
        ["Global warming", "refers to", "long-term warming"],
        ["Global warming", "encompasses", "Climate change"],
        ["Humans", "caused", "major climate changes"],
        ["Humans", "emitting", "greenhouse gases"],
        ["Greenhouse gases", "contribute to", "Global warming"],
        ["Global warming", "causes", "long-term warming"],
        ["Global warming", "causes", "rise in global temperatures"],
        ["Global warming", "causes", "flattening within a few years"]]
    llm = "gpt"
    alignedTriples = alignTriples(str(candidateTriples), llm)
    return alignedTriples