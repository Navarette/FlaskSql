from flask import Flask, render_template, send_file, make_response, url_for, Response,request,redirect
import pandas as pd
import pymssql
import matplotlib.pyplot as plt

app = Flask(__name__)

conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS',user='navarette.arnold',password='xxx123##',database='navarette.arnold')

@app.route('/', methods=['GET'])
def home():
  return render_template('home.html')

    
    

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=2223)