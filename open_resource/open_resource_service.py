import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)


def get_connection():
  conn =  sqlite3.connect('Planning_Applications_Decisions.db')
  conn.row_factory = sqlite3.Row
  return conn

def get_data_from_db(conn,table):
    cur = conn.cursor()
    cur.execute(f"select * from {table}")
    return cur.fetchall()

def get_data_from_db_where(conn, table, colume, value):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table} WHERE {colume} = ?", (value,))
    return cur.fetchall()

@app.route('/')
def index():
  conn = get_connection()
  rows = get_data_from_db(conn,"ID_table")
  conn.close()
  return render_template('index.html', rows=rows)

@app.route('/show/<Feature_ID>')
def show(Feature_ID):
  conn = get_connection()
  rows = get_data_from_db_where(conn,"category", "Feature_ID", Feature_ID)
  conn.close()
  return render_template('show.html', rows=rows, Feature_ID=Feature_ID)

@app.route('/associations')
def associations():
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    SELECT * FROM ID_table
    JOIN category ON ID_table.Feature_ID = category.Feature_ID
  """)
  rows = cur.fetchall()
  conn.close()
  
  values = [row['Value'] for row in rows if row['Value'] is not None]

  if values:
    total = sum(values)
    average = total / len(values)
    max_value = max(values)
    min_value = min(values)
  else:
    total = average = max_value = min_value = 0

  return render_template('associations.html', rows=rows, total=total, average=average, max_value=max_value, min_value=min_value)


if __name__ == '__main__':
  app.run(debug=True)