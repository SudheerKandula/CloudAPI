from flask import jsonify, make_response
from flask import Flask
import mysql.connector
import os
app = Flask(__name__)

# db_user = os.environ.get('CLOUD_SQL_USERNAME')
# db_password = os.environ.get('CLOUD_SQL_PASSWORD')
# db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
# db_connection_name = os.environ.get('CLOUD_SQL_HOST_NAME')


def get_db_connection():
    cnx = mysql.connector.connect(user='dev', password='PO9dCbn3DMzkrC90',
                                  host='35.232.245.43',
                                  database='countriesdb')
    return cnx


# method to return list a country of specific iso code
@app.route('/<isocode>')
def index(isocode):
    conn = get_db_connection()
    # this return the MYSQLCursorPrepared Object
    cursor = conn.cursor()
    query = """SELECT * FROM country WHERE iso = %s"""
    cond = isocode
    # executing a parameterized query with iso code as parameter passed at runtime
    cursor.execute(query, (cond,))
    row_headers = [x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    cursor.close()
    conn.close()
    return make_response(jsonify(json_data))


# method to return list of all countries
@app.route('/')
def homepage():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """SELECT * FROM country"""
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data = []
    # wrap the data into a dictionary
    # zipping headers as keys, column values as values
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    cursor.close()
    conn.close()
    return make_response(jsonify(json_data))


if __name__ == "__main__":
    app.run()
