# -*- coding: utf-8 -*-
"""
Created on Mon May  6 19:46:02 2019

@author: Nataliya_Pavych
"""

import plotly
from plotly.offline import plot
from plotly.offline import iplot
import plotly.graph_objs as go

import pandas as pd

df = pd.read_csv('HistoricalQuotes.csv')

trace_high = go.Scatter(
    x=df.date,
    y=df['high'],
    name = "EPAM High",
    line = dict(color = '#17BECF'),
    opacity = 0.8)

trace_low = go.Scatter(
    x=df.date,
    y=df['low'],
    name = "EPAM Low",
    line = dict(color = '#7F7F7F'),
    opacity = 0.8)

data = [trace_high,trace_low]

plotly.offline.plot({
    "data": [trace_high,trace_low],
    "layout": go.Layout(title="EPAM Stocks")
}, auto_open=True)


