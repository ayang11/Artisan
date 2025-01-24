from flask import Flask, render_template_string, session, request
from pandas import DataFrame

import charting
import helpers
import html_strings


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Artisan'

CHART_WIDTH = 2400
CHART_HEIGHT = 1200

GROUPING_OPTIONS = 'Airline','Origin','Destination'
CHART_OPTIONS = 'ASM','Seats','Flights'

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
            return render_template_string(html_strings.HOME_HTML + html_strings.add_charting_buttons(session['section']), **kwargs)
        
        if filtering.lower() == 'airline':
            if filter_value.upper() not in helpers.airlines_list(section):
                kwargs['error_filter_value']=True 
                return render_template_string(html_strings.HOME_HTML + html_strings.add_charting_buttons(session['section']), **kwargs)
                
        if filtering.lower() in ('origin','destination'):
            if filter_value.upper() not in helpers.airports_list(section):
                kwargs['error_filter_value']=True 
                return render_template_string(html_strings.HOME_HTML + html_strings.add_charting_buttons(session['section']), **kwargs)
                
        if (grouping.lower() not in ('airline','origin','destination')):
            kwargs['error_grouping']=True 
            return render_template_string(html_strings.HOME_HTML + html_strings.add_charting_buttons(session['section']), **kwargs)
            
        if (value.lower() not in ('asm','seats','flights')):
            kwargs['error_value']=True 
            return render_template_string(html_strings.HOME_HTML + html_strings.add_charting_buttons(session['section']), **kwargs)
        
        if value.lower() in ('asm','seats'):
            return render_template_string(html_strings.HOME_HTML + html_strings.add_charting_buttons(session['section']) + charting.make_bar(section, filter_col=filtering, group_col=grouping, value_col=value, filter_value=filter_value), **kwargs)
        else:
            return render_template_string(html_strings.HOME_HTML + html_strings.add_charting_buttons(session['section']) + charting.make_lines(section, filter_col=filtering, group_col=grouping, filter_value=filter_value), **kwargs)
    
    return render_template_string(html_strings.HOME_HTML + html_strings.add_charting_buttons(session['section']))


@app.route('/filtering_options')
def filtering_options():
    return render_template_string(html_strings.HOME_HTML + '<br>'.join(GROUPING_OPTIONS))

@app.route('/filter_options')
def filter_options():
    html = """<b>Airlines</b>"""
    airlines = DataFrame(dict(Airline=helpers.airlines_list(session['section']),))
    airlines['Code'] = airlines.index
    html += airlines.reindex(columns=['Code','Airline']).sort_values(['Code']).to_html(index=False)
    html +='<br>'
    
    html += """<b>Airports</b>"""
    airports = DataFrame(dict(Airport=helpers.airports_list(session['section']),))
    airports['Code'] = airports.index
    html += airports.reindex(columns=['Code','Airport']).sort_values(['Code']).to_html(index=False)
    html +='<br>'
    
    return render_template_string(html_strings.HOME_HTML + html)

@app.route('/grouping_options')
def grouping_options():
    return render_template_string(html_strings.HOME_HTML + '<br>'.join(GROUPING_OPTIONS))

@app.route('/chart_options')
def chart_options():
    return render_template_string(html_strings.HOME_HTML + '<br>'.join(CHART_OPTIONS))

@app.route('/')
def home():
    return render_template_string(html_strings.HOME_HTML)

@app.route('/europe_economy')
def europe_economy():
    session['section'] = 'Europe Economy'
    return render_template_string(html_strings.HOME_HTML + html_strings.add_charting_buttons(session['section']))

@app.route('/intercontinental_economy')
def intercontinental_economy():
    session['section'] = 'Intercontinental Economy'
    return render_template_string(html_strings.HOME_HTML + html_strings.add_charting_buttons(session['section']))

@app.route('/intercontinental_business')
def intercontinental_business():
    session['section'] = 'Intercontinental Business'
    return render_template_string(html_strings.HOME_HTML + html_strings.add_charting_buttons(session['section']))

if __name__ == '__main__':
    app.run(debug=True)