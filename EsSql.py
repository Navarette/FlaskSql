from flask import Flask, render_template, send_file, make_response, url_for, Response,request,redirect
import pandas as pd
import pymssql
import matplotlib.pyplot as plt

import io
import geopandas as gpd
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS',user='navarette.arnold',password='xxx123##',database='navarette.arnold')

@app.route('/', methods=['GET'])
def home():
  return render_template('home.html')

@app.route("/selezione", methods=["GET"])
def selezione():
    scelta = request.args['scelta']
    #in base alla scelta del radio button ti porta a diverse rotte
    if scelta == 'es1':
        return redirect(url_for('es1'))
    elif scelta == 'es2':
        return redirect(url_for('es2'))
    else:
        return redirect(url_for('es3'))   
  # 1 
@app.route("/es1", methods=["GET"])
def es1():
    global numProdotti
    query = 'select category_name,count(*) as num_prodotti from production.products INNER JOIN production.categories on production.categories.category_id = production.products.category_id group by category_name order by num_prodotti asc'
    numProdotti = pd.read_sql(query,conn)
    return render_template("es1.html",nomiColonne = numProdotti.columns.values, dati = list(numProdotti.values.tolist()))

@app.route("/grafico", methods=["GET"])
def grafico():
    #costruzione del grafico
    fig, ax = plt.subplots(figsize = (5,5))
    fig.autofmt_xdate(rotation=45)  

    x = numProdotti.category_name
    y = numProdotti.num_prodotti

    ax.bar(x,y)
    #visualizzazione grafico
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    
    return Response(output.getvalue(), mimetype='image/png')  
  # 2 
@app.route("/es2", methods=["GET"])
def es2():
    global numOrdini
    query = 'select store_name,count(*)as num_ordini from sales.orders inner join sales.stores on sales.orders.store_id = sales.stores.store_id group by store_name order by num_ordini asc'
    numOrdini = pd.read_sql(query,conn)
    return render_template("es2.html",nomiColonne = numOrdini.columns.values, dati = list(numOrdini.values.tolist()))

@app.route("/grafico1", methods=["GET"])
def grafico1():
    #costruzione del grafico
    fig, ax = plt.subplots(figsize = (10,9))
    fig.autofmt_xdate(rotation=45)  

    x = numOrdini.store_name
    y = numOrdini.num_ordini

    ax.barh(x,y)
    #visualizzazione grafico
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    
    return Response(output.getvalue(), mimetype='image/png')   
  # 3
@app.route("/es3", methods=["GET"])
def es3():
    global numProdotti
    query = 'select brand_name,count(product_name) as num_prodotti from production.products INNER JOIN production.brands on production.brands.brand_id = production.products.brand_id group by brand_name order by count(product_name)asc'
    numProdotti = pd.read_sql(query,conn)
    return render_template("es3.html",nomiColonne = numProdotti.columns.values, dati = list(numProdotti.values.tolist()))

@app.route("/grafico2", methods=["GET"])
def grafico2():
    #costruzione del grafico
    fig, ax = plt.subplots(figsize = (5,5))

    ax.pie(numProdotti.num_prodotti,labels=numProdotti.brand_name,autopct='%1.1f%%')

    #visualizzazione grafico
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    
    return Response(output.getvalue(), mimetype='image/png') 
if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=2228)