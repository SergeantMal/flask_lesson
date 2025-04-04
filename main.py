from flask import Flask, render_template
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Цифровые часы</title>
        <style>
            body {
                background-color: #0d1117;
                color: #39ff14;
                font-family: 'Courier New', Courier, monospace;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                flex-direction: column;
            }
            #date {
                font-size: 40px;
                margin-bottom: 20px;
            }
            #clock {
                font-size: 80px;
                letter-spacing: 4px;
                padding: 20px 40px;
                border: 3px solid #39ff14;
                border-radius: 10px;
                box-shadow: 0 0 20px #39ff14;
            }
        </style>
    </head>
    <body>
        <div id="date">Загрузка...</div>
        <div id="clock">Загрузка...</div>

        <script>
            function updateTime() {
                fetch('/time')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('clock').innerText = data.time;
                        document.getElementById('date').innerText = data.date;
                    });
            }
            setInterval(updateTime, 1000);
            updateTime();
        </script>
    </body>
    </html>
    '''

@app.route('/blog')
def about():
    return render_template('blog.html')

@app.route('/contacts')
def contact():
    return render_template('contacts.html')


@app.route('/time')
def get_time():
    now = datetime.now()
    return {
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%d-%m-%Y")
    }


if __name__ == '__main__':
    app.run(debug=True)
