import datetime
import os

from flask import Flask, render_template_string, session, request
from pandas import notnull, Series, DataFrame, read_excel
from plotly.subplots import make_subplots

import helpers
import html_strings
import plotly.graph_objects as go


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Artisan'

CHART_WIDTH = 2400
CHART_HEIGHT = 1200

VALUES_COLS = {'asm':'ASMs','seats':'Seats'}

def artisan_folder(*args):
    return os.path.join('C:\\','users','yanga','desktop','artisan',*args)

@helpers.memoize
def read_file(section = 'Europe Economy'):
    if section == 'Europe Economy':
        filename=artisan_folder('Intra-Europe LCC and Network Carriers 60 days - Truncated.xlsx')
    elif section in ('Intercontinental Economy','Intercontinental Business'):
        filename=artisan_folder('Inter-Continental Network Airlines 60 days - Truncated.xlsx')
        
    dm = read_excel(filename, sheet_name=section)
    dm = dm[notnull(dm['Airline Name'])]
    return dm

def origins_list(section):return dict(Series(read_file(section)['Origin Name'].values,read_file(section)['Origin Code'].values).dropna().items())
def destinations_list(section): return dict(Series(read_file(section)['Destination Name'].values,read_file(section)['Destination Code'].values).dropna().items())
def airports_list(section):
    a = origins_list(section)
    a.update(destinations_list(section))
    return a
def airlines_list(section): return dict(Series(read_file(section)['Airline Name'].values,read_file(section)['Airline Code'].values).dropna().items())

def make_bar(section, filter_col = 'Airline Code', group_col = 'Origin Code', value_col = 'Seats', filter_value = 'FR'):
    if filter_col.lower()==filter_col: filter_col = filter_col.capitalize() + ' Code'
    if group_col.lower()==group_col: group_col = group_col.capitalize() + ' Code'
    value_col = VALUES_COLS.get(value_col.lower(),value_col)
    dm = read_file(section)
    subset = dm[dm[filter_col]==filter_value]
    subset = subset[notnull(subset[value_col])]
    values = subset[value_col].groupby(subset[group_col]).sum().sort_values()
    
    fig = go.Figure(data=[go.Bar(x=values.index, y=values.values)])
    fig.update_layout(title=section,xaxis_title=group_col,yaxis_title=value_col, width=CHART_WIDTH, height=CHART_HEIGHT)
    return fig.to_html()

def make_lines(section, filter_col = 'Airline Code', group_col = 'Origin Code', filter_value = 'FR'):
    if filter_col.lower()==filter_col: filter_col = filter_col.capitalize() + ' Code'
    if group_col.lower()==group_col: group_col = group_col.capitalize() + ' Code'
    dm = read_file(section)
    dates = [x for x in dm.columns if isinstance(x,datetime.datetime)]
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

def add_charting_buttons(title):
    return '''
    <h1>%s</h1>
    <form method="POST" action="create_chart">
        <div class="charting">
            <label for="Filtering" {%% if error_filtering %%}style="color: red; font-weight: bold;"{%% endif %%}><a href="/filtering_options">Filtering:</a></label>
            <input type="text" id="filtering" name="filtering" value="{{ filtering }}">
            
            <label for="Filter" {%% if error_filter_value %%}style="color: red; font-weight: bold;"{%% endif %%}><a href="/filter_options">Filter:</a></label>
            <input type="text" id="filter_value" name="filter_value" value="{{ filter_value }}">
            
            <label for="Grouping" {%% if error_grouping %%}style="color: red; font-weight: bold;"{%% endif %%}><a href="/grouping_options">Grouping:</a></label>
            <input type="text" id="grouping" name="grouping" value="{{ grouping }}">
            
            <label for="Value" {%% if error_value %%}style="color: red; font-weight: bold;"{%% endif %%}><a href="/chart_options">Chart:</a></label>
            <input type="text" id="value" name="value" value="{{ value }}">
            
             <button type="submit">Chart</button>
        </div>
    </form>
    '''%title

@app.route('/create_chart', methods=['GET', 'POST'])
def create_chart():
    if request.method == 'POST':
        section = session['section']
        filtering = request.form['filtering'].lower()
        filter_value = request.form['filter_value'].upper()
        grouping = request.form['grouping'].lower()
        value = request.form['value'].lower()
        
        kwargs = dict(filtering=filtering,filter_value=filter_value,grouping=grouping,value=value)
        
        if (filtering.lower() not in ('airline','origin','destination')):
            kwargs['error_filtering']=True 
            return render_template_string(html_strings.HOME_HTML + add_charting_buttons(session['section']), **kwargs)
        
        if filtering.lower() == 'airline':
            if filter_value.upper() not in airlines_list(section):
                kwargs['error_filter_value']=True 
                return render_template_string(html_strings.HOME_HTML + add_charting_buttons(session['section']), **kwargs)
                
        if filtering.lower() in ('origin','destination'):
            if filter_value.upper() not in airports_list(section):
                kwargs['error_filter_value']=True 
                return render_template_string(html_strings.HOME_HTML + add_charting_buttons(session['section']), **kwargs)
                
        if (grouping.lower() not in ('airline','origin','destination')):
            kwargs['error_grouping']=True 
            return render_template_string(html_strings.HOME_HTML + add_charting_buttons(session['section']), **kwargs)
            
        if (value.lower() not in ('asm','seats','flights')):
            kwargs['error_value']=True 
            return render_template_string(html_strings.HOME_HTML + add_charting_buttons(session['section']), **kwargs)
        
        if value.lower() in ('asm','seats'):
            return render_template_string(html_strings.HOME_HTML + add_charting_buttons(session['section']) + make_bar(section, filter_col=filtering, group_col=grouping, value_col=value, filter_value=filter_value), **kwargs)
        else:
            return render_template_string(html_strings.HOME_HTML + add_charting_buttons(session['section']) + make_lines(section, filter_col=filtering, group_col=grouping, filter_value=filter_value), **kwargs)
    
    return render_template_string(html_strings.HOME_HTML + add_charting_buttons(session['section']))


@app.route('/filtering_options')
def filtering_options():
    return render_template_string(html_strings.HOME_HTML + 'Airline<br>Origin<br>Destination')

@app.route('/filter_options')
def filter_options():
    html = """<b>Airlines</b>"""
    airlines = DataFrame(dict(Airline=airlines_list(session['section']),))
    airlines['Code'] = airlines.index
    html += airlines.reindex(columns=['Code','Airline']).sort_values(['Code']).to_html(index=False)
    html +='<br>'
    
    html += """<b>Airports</b>"""
    airports = DataFrame(dict(Airport=airports_list(session['section']),))
    airports['Code'] = airports.index
    html += airports.reindex(columns=['Code','Airport']).sort_values(['Code']).to_html(index=False)
    html +='<br>'
    
    return render_template_string(html_strings.HOME_HTML + html)

@app.route('/grouping_options')
def grouping_options():
    return render_template_string(html_strings.HOME_HTML + 'Airline<br>Origin<br>Destination')

@app.route('/chart_options')
def chart_options():
    return render_template_string(html_strings.HOME_HTML + 'ASM<br>Seats<br>Flights')

@app.route('/')
def home():
    return render_template_string(html_strings.HOME_HTML)

@app.route('/europe_economy')
def europe_economy():
    session['section'] = 'Europe Economy'
    return render_template_string(html_strings.HOME_HTML + add_charting_buttons(session['section']))

@app.route('/intercontinental_economy')
def intercontinental_economy():
    session['section'] = 'Intercontinental Economy'
    return render_template_string(html_strings.HOME_HTML + add_charting_buttons(session['section']))

@app.route('/intercontinental_business')
def intercontinental_business():
    session['section'] = 'Intercontinental Business'
    return render_template_string(html_strings.HOME_HTML + add_charting_buttons(session['section']))

if __name__ == '__main__':
    app.run(debug=True)