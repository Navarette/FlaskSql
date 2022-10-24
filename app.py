from flask import Flask,render_template,request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
  return render_template('search.html')

@app.route('/result', methods=['GET'])
def result():
    # collegamento al DB
    import pandas as pd
    import pymssql
    conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS',user='navarette.arnold',password='xxx123##',database='navarette.arnold')

    # invio query al DB e ricezione informazioni
    NomeProdotto = request.args['NomeProdotto']
    query = f"select * from production.products where product.name like '{NomeProdotto}%' " #metodo che utilizza python per inserire variabili dentro una stringa f=format
    df_prodotti = pd.read_sql(query,conn)
    # visualizzare le informazioni.

    return render_template('result.html', nomiColonne = df_prodotti.columns.values, dati = list(df_prodotti.values.tolist()))
    

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=2222)