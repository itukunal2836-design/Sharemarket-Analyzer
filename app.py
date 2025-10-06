# app.py









from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from data_fetch import fetch_and_save

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    preview = None
    chart_html = None
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
            # Generate Plotly chart for Close price
            if 'Date' in df.columns and 'Close' in df.columns:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close'))
                fig.update_layout(title=f'{ticker} Closing Price', xaxis_title='Date', yaxis_title='Close', template='plotly_white')
                chart_html = pio.to_html(fig, full_html=False)
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('index.html', preview=preview, chart_html=chart_html)

if __name__ == '__main__':
    app.run(debug=True)
