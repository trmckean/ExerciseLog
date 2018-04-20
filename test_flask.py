# Testing flask
from flask import Flask
from flask import render_template
from SQLiteDatabase import Database

app = Flask(__name__)


@app.route("/")
def hello():
    db = Database()
    max_pace = db.get_max_pace()
    user = {'username': 'Tyler'}
    return render_template('index.html', title='Home', user=user, pace=max_pace)


if __name__ == "__main__":
    app.run()
