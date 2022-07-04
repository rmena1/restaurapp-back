import requests
import json
from . import utils

from flask import (
    Blueprint, jsonify
)

bp = Blueprint('routes', __name__, url_prefix='/')

@bp.route('/get_all')
def get_all():
    data = utils.get_data()
    data = utils.order_by_date(data)
    data = utils.limit_data(data, 300)
    return jsonify(data)

# get data by date range
@bp.route('/get_by_date/<date_from>/<date_to>')
def get_by_date(date_from, date_to):
    data = utils.get_data()
    filtered_data = [d for d in data if d['date_closed'].split(' ')[0] >= date_from and d['date_closed'].split(' ')[0] <= date_to]
    ordered_data = utils.order_by_date(filtered_data)
    return jsonify(ordered_data)

# get data by exact date
@bp.route('/get_by_date/<date>')
def get_by_exact_date(date):
    data = utils.get_data()
    filtered_data = [d for d in data if d['date_closed'].split(' ')[0] == date]
    ordered_data = utils.order_by_date(filtered_data)
    return jsonify(ordered_data)
