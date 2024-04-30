from transformers import AutoTokenizer
import transformers
import torch
from transformers import pipeline
import os

model = "meta-llama/Llama-2-7b-chat-hf" # meta-llama/Llama-2-7b-hf

tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token=True)

llama_pipeline = pipeline(
    "text-generation",  # LLM task
    model=model,
    torch_dtype=torch.float32,
    device_map="auto",
)

def get_llama_response(prompt: str) -> str:
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
    

prompt_task_1 = 'You will identify the named entities in the content and then extract the relations between them. Focus on these named entities if they occur in the text: '
named_entities = 'human activities, emissions, greenhouse gas, CO2, climate change, global warming, weather, adaptation, implementation, action, mitigation, policies, laws, climate goals, risks, impacts, losses, damages'
promt_task_2 = 'Based on the provided sentences, you will return triples, which are formatted as [named entity A, relation, named entity B]. \nSTART of the sentences:\n'
prompt_task = prompt_task_1 + named_entities + promt_task_2
#prompt_task_end = '\nEND of the sentences.\nThe extracted triples formatted like [named entity A, relation, named entity B] are:'
#sentences = 'A Current Status and Trends Observed Warming and its Causes A.1 Human activities, principally through emissions of greenhouse gases, have unequivocally caused global warming, with global surface temperature reaching 1.1°C above 1850–1900 in 2011–2020. Global greenhouse gas emissions have continued to increase, with unequal historical and ongoing contributions arising from unsustainable energy use, land use and land-use change, lifestyles and patterns of consumption and production across regions, between and within countries, and among individuals (high confidence). {2.1, Figure 2.1, Figure 2.2}.'
#prompt_task = 'Extract the relations from a given text regarding these entities: Human activities, Emissions, Greenhouse Gas, Global Warming, Climate Change. \nSTART of Text\n'
prompt_task_end = '\nEND of Text\nFormat the relations in this format [named entity A, relation, named entity B]'
sentences = 'Human activities, principally through emissions of greenhouse gases, have unequivocally caused global warming, with global surface temperature reaching 1.1°C above 1850–1900 in 2011–2020. Global greenhouse gas emissions have continued to increase, with unequal historical and ongoing contributions arising from unsustainable energy use, land use and land-use change, lifestyles and patterns of consumption and production across regions, between and within countries, and among individuals (high confidence).'
prompt = prompt_task + sentences + prompt_task_end 

# task = 'Given these entities: ' + named_entities + \
#     ' identify relationships and other named entities from this given content: ' + sentences + \
#     ' Not all given entities may appear in the content. \
#     Format your output as triples [named entity A, relation, named entity B]'


# task = 'You will perform the open information extraction task. \
#     You will identify the named entities in the content and \
#     then extract the relations between them. \
#     Based on the provided testimony, you will return triples, \
#     which are formatted as [named entity A, relation, named entity B]. \
#     START of the testimony:' + sentences + \
#     'END of the testimony. The extracted triples formatted as \
#     [named entity A, relation, named entity B] are:'

#get_llama_response(task)


directory = 'vocabs'
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        with open(os.path.join(directory, filename)) as vocab:
            named_entities = vocab.read()
    #data_directory = 'Headline Statements/reduced'
    data_directory = 'Media/reduced'
    output_directory = data_directory + '/output'
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    for data_filename in os.listdir(data_directory):
        if data_filename.endswith('.txt'):
            with open(os.path.join(data_directory, data_filename)) as data:
                content = data.read()  
            task = 'You will perform the open information extraction task. \
                You will identify the named entities in the content and \
                then extract the relations between them. \
                Based on the provided testimony, you will return triples, \
                which are formatted as [named entity A, relation, named entity B]. \
                START of the testimony:' + content + \
                'END of the testimony. The extracted triples formatted as \
                [named entity A, relation, named entity B] are:'
            response = get_llama_response(task)
            output = open(os.path.join(output_directory, filename + data_filename),'w')
            output.write(response)
