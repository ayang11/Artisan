HOME_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Artisan Partners</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f0f0f0;
            height: 100vh;
        }

        .button-container {
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }

        .button {
            padding: 15px 30px;
            font-size: 16px;
            color: white;
            background-color: #808080; /* Gray color */
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .button:hover {
            background-color: #696969; /* Darker gray on hover */
        }

        .content {
            margin-top: 50px;
            text-align: center;
            color: #333;
        }
    </style>
</head>
<body>
    <a href="/">    <img src="{{ url_for('static', filename='artisan.png') }}" alt="Artisan">    </a>
    <div class="button-container">
        <a href="/europe_economy" class="button">Europe Economy</a>
        <a href="/intercontinental_economy" class="button">Intercontinental Economy</a>
        <a href="/intercontinental_business" class="button">Intercontinental Business</a>
    </div>

</body>
</html>
'''

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
