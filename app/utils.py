from flask import current_app as app
import requests
import json

def get_data():
    print('get_data()')
    data = requests.get('https://storage.googleapis.com/backupdatadev/ejercicio/ventas.json')
    print('data ready')
    return json.loads(data.content)