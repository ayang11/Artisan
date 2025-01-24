import datetime

from pandas import notnull
from plotly.subplots import make_subplots

import helpers
import plotly.graph_objects as go


CHART_WIDTH = 2400
CHART_HEIGHT = 1200

VALUES_COLS = {'asm':'ASMs','seats':'Seats'}

def make_bar(section, filter_col = 'Airline Code', group_col = 'Origin Code', value_col = 'Seats', filter_value = 'FR'):
    if filter_col.lower()==filter_col: filter_col = filter_col.capitalize() + ' Code'
    if group_col.lower()==group_col: group_col = group_col.capitalize() + ' Code'
    value_col = VALUES_COLS.get(value_col.lower(),value_col)
    dm = helpers.read_file(section)
    subset = dm[dm[filter_col]==filter_value]
    subset = subset[notnull(subset[value_col])]
    values = subset[value_col].groupby(subset[group_col]).sum().sort_values()
    
    fig = go.Figure(data=[go.Bar(x=values.index, y=values.values)])
    fig.update_layout(title=section,xaxis_title=group_col,yaxis_title=value_col, width=CHART_WIDTH, height=CHART_HEIGHT)
    return fig.to_html()

def make_lines(section, filter_col = 'Airline Code', group_col = 'Origin Code', filter_value = 'FR'):
    if filter_col.lower()==filter_col: filter_col = filter_col.capitalize() + ' Code'
    if group_col.lower()==group_col: group_col = group_col.capitalize() + ' Code'
    dm = helpers.read_file(section)
    dates = sorted([x for x in dm.columns if isinstance(x,datetime.datetime)])
    subset = dm[dm[filter_col]==filter_value]
    for col in dates:
        subset = subset[notnull(subset[col])]
    
    groups = sorted(subset[group_col].unique())
    fig = make_subplots(rows=1, cols=len(groups), subplot_titles=groups)
    mins, maxs = 0, 0
    for num,group in enumerate(groups):
        group_series = subset[subset[group_col]==group].reindex(columns=dates).sum()
        fig.add_trace(go.Scatter(x=group_series.index, y=group_series.values),row=1, col=1+num)
        if num>0:
            fig.update_yaxes(showticklabels=False,row=1, col=1+num)
        
        mins = min(group_series.min(),mins)
        maxs = max(group_series.max(),maxs)
        
    for num,group in enumerate(groups):
        fig.update_yaxes(range=(mins,maxs), row=1, col=1+num)
    
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(title_text=f'{section} {group_col} {helpers.to_dateprint(min(dates))} - {helpers.to_dateprint(max(dates))} ',
                      showlegend=False, width=CHART_WIDTH, height=CHART_HEIGHT)
    return fig.to_html()