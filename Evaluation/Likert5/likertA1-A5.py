import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def survey(results, category_names, title):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*. The order is assumed
        to be from 'Strongly disagree' to 'Strongly aisagree'
    category_names : list of str
        The category labels.
    """
    
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    middle_index = data.shape[1]//2
    offsets = data[:, range(middle_index)].sum(axis=1) + data[:, middle_index]/2
    

    # Color Mapping
    likert_colors = ['firebrick','lightcoral','gainsboro','cornflowerblue', 'darkblue']
    

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
    ax.set_xlim(-45, 45)
    ax.set_xticks(np.arange(-45, 46, 10))
    ax.xaxis.set_major_formatter(lambda x, pos: str(abs(int(x))))

    # Y Axis
    ax.invert_yaxis()
    
    # Remove spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(True)
    
    # Ledgend
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')
    
    # Set Background Color
    fig.set_facecolor('#FFFFFF')
    ax.set_title(title, fontsize = 20, pad=40)
    fig.tight_layout()
    return fig, ax

answerOptions = ["A5", "A4", "A3", "A2", "A1"]
category_names = ['Strongly disagree', 'Disagree',
                  'Neither agree nor disagree', 'Agree', 'Strongly agree']

files = ["I think a scientific accuracy score is ...", "I think the tool in the current state is ...", "I would like to use this tool as a ...", "I would like to use this tool to check ...", "I am experienced in the following area ..."] 

for name in files:
    name = "I would like to use this tool to check ..."
    data = pd.read_csv(name + ".csv")

    results = {}
    for header in data.columns:
        results[header] = []
        for answerOption in answerOptions:
            count = 0
            for datapoint in data[header]:
                if datapoint == answerOption:
                    count = count + 1
            results[header].append(count)

    fig, ax = survey(results, category_names, name)

    plt.show()
    break
