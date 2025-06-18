import matplotlib.pyplot as plt

fig, ax = plt.subplots()

answerOptions = ['The optimal method for extracting triples is currently unclear.', 'LLMs have limitations and should not be used without proper checks to identify non-reproducible or hallucinated triples. ', 'Scientific accuracy checks must take into account the context of statements, which cannot be represented by a single triple.', 'This tool is more likely to be used as an integrated rather than a standalone tool. ', 'As long as ”a perfect algorithm to check against the truth” is not achievable: - Having an indication of what is more or less likely to be accurate is already helpful. ']
counts = [9,16,13,4,8]
#answerOptions = {'Handling semantic alignment of natural language.': [0, 0, 6], 'Handling LLM hallucinations and lacking reproducibility.': [0, 0, 9], 'Fully automated triple extraction. ': [0, 0, 0], 'Keeping the context of statements, especially in empirical research.': [0, 0, 11], 'Making statements about statements to show their confidence or time validity. ': [0, 0, 1]}
counts = [6,9,0,11,1]

answerOptions = ['1','2','3','4','5']

bar_colors = ['cornflowerblue', 'cornflowerblue', 'cornflowerblue', 'cornflowerblue', 'cornflowerblue']
#label=bar_labels, 
ax.bar(answerOptions, counts, color=bar_colors)

ax.set_ylabel('Count')
#ax.legend(title='Statement')

plt.show()