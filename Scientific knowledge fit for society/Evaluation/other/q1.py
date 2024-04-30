import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# answerOptions = ["A6", "A5", "A4", "A3", "A2", "A1"]
# data = pd.read_csv("I think a scientific accuracy score is.csv")
# category_names = ['Strongly disagree', 'Disagree',
#                   'Neither agree nor disagree', 'Agree', 'Strongly agree']

category_names = ["no", "uncertain", "yes"]
answerOptions = ["N", "U", "Y"]
data = pd.read_csv("Q1Misinformation.csv")

results = {}
for header in data.columns:
    results[header] = []
    for answerOption in answerOptions:
        count = 0
        for datapoint in data[header]:
            if datapoint == answerOption:
                count = count + 1
        results[header].append(count) 

def survey(results, category_names):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*. The order is assumed
        to be from 'disagree' to 'agree'
    category_names : list of str
        The category labels.
    """
    
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    middle_index = data.shape[1]//2
    offsets = data[:, range(middle_index)].sum(axis=1) + data[:, middle_index]/2
    

    # Color Mapping
    category_colors = plt.get_cmap('coolwarm_r')(
        np.linspace(0.15, 0.85, data.shape[1]))
    #likert_colors = ['firebrick','lightcoral','gainsboro','cornflowerblue', 'darkblue']
    likert_colors = ['lightcoral', 'gainsboro', 'cornflowerblue']

    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plot Bars
    for i, (colname, color) in enumerate(zip(category_names, likert_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths - offsets
        rects = ax.barh(labels, widths, left=starts, height=0.6,
                        label=colname, color=color)

    # Add Zero Reference Line
    ax.axvline(0, linestyle='--', color='black', alpha=.25)
    
    # X Axis
    # ax.set_xlim(-45, 45)
    # ax.set_xticks(np.arange(-45, 46, 10))
    ax.set_xlim(-25, 25)
    ax.set_xticks(np.arange(-25, 26, 10))
    ax.xaxis.set_major_formatter(lambda x, pos: str(abs(int(x))))

    # Y Axis
    ax.invert_yaxis()
    #ax.set_ylim(-5, 15)
    
    # Remove spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(True)
    
    # Ledgend
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')
    
    # Set Background Color
    fig.set_facecolor('#FFFFFF')
    #ax.set_title("Misinformation ...", fontsize = 20, pad=40)
    ax.set_title("Questions about the approach:", fontsize = 20, pad=40)
    fig.tight_layout()
    return fig, ax


results = {'Is this approach up to date?': [0, 3, 14], 'Is this workflow efficient?': [0, 10, 0], 'Would you use this tool?': [1, 2, 10], 'Statement 1 - Do you agree?': [1, 8, 0], 'Statement 2 - Do you agree?': [7, 4, 1], 'Statement 3 - Do you agree?': [2, 5, 1], 'Statement 4 - Do you agree?': [1, 5, 3]}
#1 The best way to extract triples is achieved through NER with a domain specific model.
#2 Using an LLM to extract triples is a quick, easy and quite good solution.
#3 The path length is impactful to evaluate a claimed relation between A and B.
#4 The degree of the nodes on these paths is impactful to evaluate a claimed relation between A and B.
fig, ax = survey(results, category_names)


plt.show()
