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