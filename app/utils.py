from flask import current_app as app
import requests
import json

def get_data():
    data = requests.get('https://storage.googleapis.com/backupdatadev/ejercicio/ventas.json')
    return json.loads(data.content)