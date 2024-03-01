import sqlite3
from flask import Flask, render_template, request

# app = Flask(__name__, instance_relative_config=True) creates the Flask instance. 
# __name__ is the name of the current Python module. 
app = Flask(__name__)
 #global instance of connection
# App Routing means mapping the URLs to a specific function that will handle the logic for that URL.
# In our application, the URL (“/”) is associated with the root URL.

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