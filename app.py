from flask import Flask, render_template, request, session
import requests

app = Flask(__name__)
import os
API_KEY = os.environ.get('API_KEY')  # Securely load from environment
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"
@app.route('/', methods=['GET', 'POST'])
def convert():
    currencies = ["USD", "EUR", "INR", "GBP", "JPY", "AUD", "CAD"]  # Add more as needed
    converted_amount = None
    rate = None
    from_currency = to_currency = None

    if request.method == 'POST':
        amount = float(request.form['amount'])
        from_currency = request.form['from']
        to_currency = request.form['to']
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        data = requests.get(url).json()
        rate = data['rates'][to_currency]
        converted_amount = round(amount * rate, 2)

        # Save history in session
        history = session.get('history', [])
        history.append({
            'amount': amount,
            'from': from_currency,
            'to': to_currency,
            'converted': converted_amount,
            'rate': rate
        })
        session['history'] = history

    return render_template('converter.html',
                           currencies=currencies,
                           converted_amount=converted_amount,
                           rate=rate,
                           from_currency=from_currency,
                           to_currency=to_currency,
                           history=session.get('history', []))
