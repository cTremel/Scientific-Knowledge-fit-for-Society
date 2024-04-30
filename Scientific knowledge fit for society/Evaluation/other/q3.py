import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


answerOptions = ["A7", "A6", "A5", "A4", "A3", "A2", "A1"]
data = pd.read_csv("Q3ranking.csv")
category_names = ['A7', 'A6',
                  'A5', 'A4', 'A3', 'A2', 'A1']

results = {}
for header in data.columns:
    results[header] = []
    for answerOption in answerOptions:
        count = 0
        for datapoint in data[header]:
            if datapoint == answerOption:
                count = count + 1
        results[header].append(count) 

print(results)

def survey(results, category_names):
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
    category_colors = plt.get_cmap('coolwarm_r')(
        np.linspace(0.15, 0.85, data.shape[1]))
    #likert_colors = ['firebrick','lightcoral','gainsboro','cornflowerblue', 'darkblue']
    #likert_colors = ['lightcoral', 'gainsboro', 'cornflowerblue']

    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plot Bars
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
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
    ax.set_title("Please rank the following options in order of importance for your acceptance of a scientific accuracy score.", fontsize = 20, pad=40)
    fig.tight_layout()
    return fig, ax


fig, ax = survey(results, category_names)


plt.show()

# A7 = 4*6+9*5+12*4+8*3+4*2+3*1+3*0 = 152
# A6 = 4*6+11*5+6*4+9*3+6*2+2*1+5*0 = 144
# A5 = 19*6+9*5+11*4+1*3+2*2+1*1+0*0 = 211
# A4 = 2*6+1*5+1*4+4*3+9*2+10*1+16*0 = 61
# A3 = 10*6+12*5+7*4+6*3+4*2+3*1+1*0 = 177
# A2 = 2*6+1*5+3*4+13*3+8*2+13*1+3*0 = 97
# A1 = 2*6+0*5+3*4+2*3+10*2+11*1+15*0 = 61
# {'Rank 1': [4, 4, 19, 2, 10, 2, 2], 
#  'Rank 2': [9, 11, 9, 1, 12, 1, 0],
#  'Rank 3': [12, 6, 11, 1, 7, 3, 3], 
#  'Rank 4': [8, 9, 1, 4, 6, 13, 2], 
#  'Rank 5': [4, 6, 2, 9, 4, 8, 10], 
#  'Rank 6': [3, 2, 1, 10, 3, 13, 11], 
#  'Rank 7': [3, 5, 0, 16, 1, 3, 15]}
