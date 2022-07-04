from flask import current_app as app
import requests
import json

def get_data():
    data = requests.get('https://storage.googleapis.com/backupdatadev/ejercicio/ventas.json')
    return json.loads(data.content)

def order_by_date(data):
    return sorted(data, key=lambda k: k['date_closed'], reverse=True)
