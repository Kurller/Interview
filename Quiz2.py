from flask import Flask, render_template
import pymysql

app = Flask(__name__)

# Database Configuration
db = pymysql.connect(host='localhost',
                     user='postgres',
                     password='1234',
                     database='koladb',
                     cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index2():
    return render_template('index2.html')
@app.route('/local_government/<local_government_id>')
def local_government_results(local_government_id):
    with db.cursor() as cursor:
        
        query = """
            SELECT party_abbreviation, SUM(party_score) as total_score
            FROM announced_pu_results
            WHERE polling_unit_uniqueid IN (
                SELECT polling_unit_uniqueid
                FROM polling_unit
                WHERE lga_id = %s
            )
            GROUP BY party_abbreviation
        """
        cursor.execute(query, (local_government_id,))
        results = cursor.fetchall()

        # Convert the results to a dictionary for easy rendering in the template
        total_results = {result['party_abbreviation']: result['total_score'] for result in results}

        return render_template('index2.html', results=total_results)


if __name__ == '__main__':
    app.run(debug=True)
