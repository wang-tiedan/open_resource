import sqlite3, logging, os

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

@app.route('/associations/<Feature_ID>')
def associations(Feature_ID):
  try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
      SELECT ID_table.Feature_ID, ID_table.DateCode, ID_table.Measurement,ID_table.Value, 
      ID_table.by_Development_Type, category.ID, category.Value AS 'Cvalue', 
      category.DateCode AS 'CDateCode', category.by_category
      FROM ID_table
      JOIN category ON ID_table.Feature_ID = category.Feature_ID 
      WHERE category.Feature_ID = ?
    """, (Feature_ID,))
    rows = cur.fetchall()
    cur.execute("""      
      SELECT SUM(category.Value) FROM ID_table
      JOIN category ON ID_table.Feature_ID = category.Feature_ID 
      WHERE category.Feature_ID = ?""", (Feature_ID,))
    total = cur.fetchone()["SUM(category.Value)"]
    cur.execute("""      
      SELECT AVG(category.Value) FROM ID_table
      JOIN category ON ID_table.Feature_ID = category.Feature_ID 
      WHERE category.Feature_ID = ?""", (Feature_ID,))
    average =  cur.fetchone()["AVG(category.Value)"]
    cur.execute("""      
      SELECT MAX(category.Value) FROM ID_table
      JOIN category ON ID_table.Feature_ID = category.Feature_ID 
      WHERE category.Feature_ID = ?""", (Feature_ID,))
    max_value =  cur.fetchone()["MAX(category.Value)"]
    cur.execute("""      
      SELECT MIN(category.Value) FROM ID_table
      JOIN category ON ID_table.Feature_ID = category.Feature_ID 
      WHERE category.Feature_ID = ?""", (Feature_ID,))
    min_value =  cur.fetchone()["MIN(category.Value)"]
    print(total)
    conn.close()
  except sqlite3.DatabaseError as e:
    app.logger.error(f"Database error: {e}")
    return render_template('error.html'), 500
  except Exception as e:
    app.logger.error(f"Internal error: {e}")
    return render_template('error.html'), 500
  return render_template('associations.html', rows=rows, average=average,total=total,max_value=max_value,min_value=min_value)

@app.errorhandler(404)
def not_found_error(error):
  return render_template('404.html'), 404 

@app.errorhandler(500)
def internal_error(error):
  return render_template('500.html'), 500  

if __name__ == '__main__':
  app.run(debug=False)
  app.run(debug=DEBUG_MODE)