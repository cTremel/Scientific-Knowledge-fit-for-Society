import plotly.graph_objects as go
import pandas as pd

#top_labels = ['Strongly<br>agree', 'Agree', 'Neutral', 'Disagree', 'Strongly<br>disagree']
top_labels = ["no", "uncertain", "yes"]
answerOptions = ["N", "U", "Y"]

data = pd.read_csv("Q1Misinformation.csv")
answers = {}
for header in data.columns:
    answers[header] = []
    for answerOption in answerOptions:
        count = 0
        for datapoint in data[header]:
            if datapoint == answerOption:
                count = count + 1
        answers[header].append(count)   

d = {'Question': data.columns}

# for i in range(len(answerOptions)):
#     d[top_labels[i]] = answers[answerOptions[i]]

colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
          'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
          'rgba(190, 192, 213, 1)']

print(answers)
x_data = []
for header in data.columns:
    x_data.append(answers[header])



# for i in range(len(answerOptions)):
#     x_data.append(answers[answerOptions[i]])
#print(x_data)
# x_data = [[21, 30, 21, 16, 12],
#           [24, 31, 19, 15, 11],
#           [27, 26, 23, 11, 13],
#           [29, 24, 15, 18, 14]]

y_data = data.columns
# y_data = ['The course was effectively<br>organized',
#           'The course developed my<br>abilities and skills ' +
#           'for<br>the subject', 'The course developed ' +
#           'my<br>ability to think critically about<br>the subject',
#           'I would recommend this<br>course to a friend']

fig = go.Figure()

for i in range(0, len(x_data[0])):
    for xd, yd in zip(x_data, y_data):
        fig.add_trace(go.Bar(
            x=[xd[i]], y=[yd],
            orientation='h',
            marker=dict(
                color=colors[i],
                line=dict(color='rgb(248, 248, 249)', width=1)
            )
        ))

fig.update_layout(
    xaxis=dict(
        showgrid=True,
        showline=True,
        showticklabels=True,
        zeroline=True,
        domain=[0, 1]
    ),
    yaxis=dict(
        showgrid=True,
        showline=True,
        showticklabels=False,
        zeroline=True,
    ),
    barmode='stack',
    paper_bgcolor='rgb(248, 248, 255)',
    plot_bgcolor='rgb(248, 248, 255)',
    margin=dict(l=120, r=10, t=140, b=80),
    showlegend=False,
)

annotations = []

for yd, xd in zip(y_data, x_data):
    # labeling the y-axis
    annotations.append(dict(xref='paper', yref='y',
                            x=0.14, y=yd,
                            xanchor='right',
                            text=str(yd),
                            font=dict(family='Arial', size=14,
                                      color='rgb(67, 67, 67)'),
                            showarrow=False, align='right'))
    # labeling the first percentage of each bar (x_axis)
    annotations.append(dict(xref='x', yref='y',
                            x=xd[0] / 2, y=yd,
                            text=str(xd[0]) + '%',
                            font=dict(family='Arial', size=14,
                                      color='rgb(248, 248, 255)'),
                            showarrow=False))
    # labeling the first Likert scale (on the top)
    if yd == y_data[-1]:
        annotations.append(dict(xref='x', yref='paper',
                                x=xd[0] / 2, y=1.1,
                                text=top_labels[0],
                                font=dict(family='Arial', size=14,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False))
    space = xd[0]
    for i in range(1, len(xd)):
            # labeling the rest of percentages for each bar (x_axis)
            annotations.append(dict(xref='x', yref='y',
                                    x=space + (xd[i]/2), y=yd,
                                    text=str(xd[i]) + '%',
                                    font=dict(family='Arial', size=14,
                                              color='rgb(248, 248, 255)'),
                                    showarrow=False))
            # labeling the Likert scale
            if yd == y_data[-1]:
                annotations.append(dict(xref='x', yref='paper',
                                        x=space + (xd[i]/2), y=1.1,
                                        text=top_labels[i],
                                        font=dict(family='Arial', size=14,
                                                  color='rgb(67, 67, 67)'),
                                        showarrow=False))
            space += xd[i]

fig.update_layout(annotations=annotations)

fig.show()