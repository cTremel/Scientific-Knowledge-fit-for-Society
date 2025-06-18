import numpy as np
import pandas as pd
import plotly.graph_objects as go

data = pd.read_csv("Q1Misinformation.csv")

question = []
answerOptions = ["N", "U", "Y"]
answerOptionsName = ["no", "uncertain", "yes"]
answers = {}

for answerOption in answerOptions:
    answers[answerOption] = []
    for header in data.columns:
        count = 0
        for datapoint in data[header]:
            if datapoint == answerOption:
                count = count + 1
        answers[answerOption].append(count)
   
d = {'Question': data.columns}
for i in range(len(answerOptions)):
    d[answerOptionsName[i]] = answers[answerOptions[i]]
    
print(d)

df = pd.DataFrame(d)

fig = go.Figure()
middle = round(len(answerOptions)/2)
print(len(answerOptions))
print(5/2)
for col in df.columns[1:2]:
    fig.add_trace(go.Bar(x=-df[col].values,
                         y=df['Question'],
                         marker_color="firebrick",
                         orientation='h',
                         name=col,
                         customdata=df[col],
                         hovertemplate = "%{y}: %{customdata}"),
                         )
for col in df.columns[2:3]:
    fig.add_trace(go.Bar(x= df[col],
                         y =df['Question'],
                         marker_color="steelblue",
                         orientation='h',
                         name= col,
                         hovertemplate="%{y}: %{x}")) 
for col in df.columns[3:]:
    fig.add_trace(go.Bar(x= df[col],
                         y =df['Question'],
                         marker_color="forestgreen",
                         orientation='h',
                         name= col,
                         hovertemplate="%{y}: %{x}"))    

fig.update_layout(barmode='relative', 
                  height=400, 
                  width=700, 
                  yaxis_autorange='reversed',
                  bargap=0.01,
                  legend_orientation ='h',
                  legend_x=-0.05, legend_y=1.1
                 )

#fig.write_html('first_figure.html', auto_open=True)
#fig.show()