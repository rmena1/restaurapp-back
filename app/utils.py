from flask import current_app as app
import requests
import json

def get_data():
    print('GETTING DATA')
    data = requests.get('https://storage.googleapis.com/backupdatadev/ejercicio/ventas.json')
    print('DATA:', data)
    return json.loads(data.content)