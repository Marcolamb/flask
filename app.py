from flask import Flask, request, render_template, jsonify
import requests
import pandas as pd
import sqlite3
import json
from flask_cors import CORS


app = Flask(__name__) 
cors = CORS(app)




@app.route('/')
def index():
    return render_template('index.html')



@app.route('/graph')
def graph():

    conn = sqlite3.connect('test.db')

    df = pd.read_sql_query('SELECT * FROM countries', conn) # transform df into dict
    df_dict = df.to_dict('records')

    conn.close()
    return jsonify(df_dict)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
        


    
    
    
