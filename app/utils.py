from flask import current_app as app
import requests
import json

def get_data():
    data = requests.get('https://storage.googleapis.com/backupdatadev/ejercicio/ventas.json')
    return json.loads(data.content)

def order_by_date(data):
    return sorted(data, key=lambda k: k['date_closed'], reverse=True)

def filter_by_date_range(data, date_from, date_to):
    return [d for d in data if d['date_closed'].split(' ')[0] >= date_from and d['date_closed'].split(' ')[0] <= date_to]

#limit data quantity
def limit_data(data, limit):
    return data[:limit]
