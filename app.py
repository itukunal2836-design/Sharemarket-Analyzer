# app.py









from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pandas as pd
from data_fetch import fetch_and_save

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    preview = None
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        start = request.form.get('start')
        end = request.form.get('end')
        try:
            path = fetch_and_save(ticker, start, end)
            flash(f'Data for {ticker} saved to {path}', 'success')
            # Load first 10 rows for preview
            df = pd.read_csv(path)
            preview = df.head(10).to_html(classes='table table-striped', index=False)
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('index.html', preview=preview)

if __name__ == '__main__':
    app.run(debug=True)
