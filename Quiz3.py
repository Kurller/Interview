from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Database Configuration
db = pymysql.connect(host='localhost',
                     user='postgres',
                     password='1234',
                     database='koladb',
                     cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index3():
    return render_template('index3.html')

@app.route('/new_polling_unit', methods=['GET', 'POST'])
def new_polling_unit():
    if request.method == 'POST':
        polling_unit_name = request.form['polling_unit_name']
        party_results = {}
        for party in ['PDP', 'APC', 'AA', 'APGA', 'SDP']:
            party_results[party] = request.form[f'{party}_score']

        # Insert party results for the new polling unit into the database
        with db.cursor() as cursor:
            query = """
                INSERT INTO announced_pu_results (polling_unit_uniqueid, party_abbreviation, party_score)
                VALUES (%s, %s, %s)
            """
            for party, score in party_results.items():
                cursor.execute(query, (polling_unit_name, party, score))
            db.commit()

        return redirect(url_for('index3'))

    return render_template('new_polling_unit.html')

if __name__ == '__main__':
    app.run(debug=True)
