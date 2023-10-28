from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def get_polling_unit_results():
    connection = sqlite3.connect('koladb.db')  
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM announced_pu_results')
    results = cursor.fetchall()
    connection.close()
    return results

@app.route('/')
def index():
    polling_unit_results = get_polling_unit_results()
    return render_template('index.html', results=polling_unit_results)

if __name__ == '__main__':
    app.run(debug=True)
