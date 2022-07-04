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

# get useful info from data between date range
@bp.route('/get_info/<date_from>/<date_to>')
def get_info(date_from, date_to):
    data = utils.get_data()
    filtered_data = [d for d in data if d['date_closed'].split(' ')[0] >= date_from and d['date_closed'].split(' ')[0] <= date_to]
    # get total sales
    total_sales = sum([d['total'] for d in filtered_data])
    # avarage total sales
    avarage_sales = total_sales / len(filtered_data)
    # avarege diners
    avarage_diners = sum([d['diners'] for d in filtered_data]) / len(filtered_data)
    return jsonify({'total_sales': total_sales, 'avarage_sales': avarage_sales, 'avarage_diners': avarage_diners})
