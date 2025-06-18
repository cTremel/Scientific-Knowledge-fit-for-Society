import os

directory = 'vocabs'
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        with open(os.path.join(directory, filename)) as vocab:
            named_entities = vocab.read()
    data_directory = 'Headline Statements/reduced'
    output_directory = data_directory + '/output'
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    for data_filename in os.listdir(data_directory):
        if data_filename.endswith('.txt'):
            with open(os.path.join(data_directory, data_filename)) as data:
                content = data.read()  
        
        output = open(os.path.join(output_directory, filename + data_filename),'w')
        output.write("named entities: \n" + named_entities + "\nContent:\n" + content)

