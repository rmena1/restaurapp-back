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
    filtered_data = utils.filter_by_date_range(data, date_from, date_to)
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
    filtered_data = utils.filter_by_date_range(data, date_from, date_to)
    # get total sales
    total_sales = sum([d['total'] for d in filtered_data])
    # avarage total sales
    avarage_sales = total_sales / len(filtered_data)
    # avarege diners
    avarage_diners = sum([d['diners'] for d in filtered_data]) / len(filtered_data)
    return jsonify({'total_sales': int(total_sales), 'avarage_sales': f'{avarage_sales:.2f}', 'avarage_diners': f'{avarage_diners:.2f}'})

# get category of products sold in date range
@bp.route('/get_category/<date_from>/<date_to>')
def get_category(date_from, date_to):
    data = utils.get_data()
    filtered_data = utils.filter_by_date_range(data, date_from, date_to)
    # get category of products sold
    category = []
    for d in filtered_data:
        for product in d['products']:
            if product['category'] not in category:
                category.append(product['category'])
    return jsonify(category)

# get products of category sold in date range
@bp.route('/get_products/<category>/<date_from>/<date_to>')
def get_products(category, date_from, date_to):
    data = utils.get_data()
    filtered_data = utils.filter_by_date_range(data, date_from, date_to)
    # get products of category sold
    products = []
    for d in filtered_data:
        for product in d['products']:
            if product['category'] == category:
                if product['name'] not in products:
                    products.append(product['name'])
    return jsonify(products)

# get product sales between date range filtered by category
@bp.route('/get_product_sales/<category>/<date_from>/<date_to>')
def get_product_sales(date_from, date_to, category):
    data = utils.get_data()
    filtered_data = utils.filter_by_date_range(data, date_from, date_to)
    products = []
    for d in filtered_data:
        for p in d['products']:
            if p['category'] == category:
                products.append(p)
    # add sales of each product
    sales = {}
    quantity = {}
    for p in products:
        if p['name'] in sales:
            sales[p['name']] += (p['price'] * p['quantity'])
            quantity[p['name']] += p['quantity']
        else:
            sales[p['name']] = (p['price'] * p['quantity'])
            quantity[p['name']] = p['quantity']
    final_sales = []
    for s in sales:
        final_sales.append({'name': s, 'sales': sales[s], 'quantity': quantity[s]})
    return jsonify(final_sales)

# get product, category or total sales for each day between date range
@bp.route('/get_daily_sales/<category>/<product>/<date_from>/<date_to>')
def get_daily_sales(date_from, date_to, category, product):
    data = utils.get_data()
    filtered_data = utils.filter_by_date_range(data, date_from, date_to)
    days = {}
    for d in filtered_data:
        for p in d['products']:
            if (p['category'] == category and p['name'] == product) or (product == 'Todo' and p['category'] == category) or (product == 'Todo' and category == 'Todo'):
                if d['date_closed'].split(' ')[0] in days:
                    days[d['date_closed'].split(' ')[0]] += (p['price'] * p['quantity'])
                else:
                    days[d['date_closed'].split(' ')[0]] = (p['price'] * p['quantity'])
    final_sales = []
    for d in days:
        final_sales.append({'date': d, 'sales': days[d]})
    # order by date
    final_sales = sorted(final_sales, key=lambda k: k['date'])
    return jsonify(final_sales)

# get percentage of sales for each category between date range
@bp.route('/get_category_sales/<date_from>/<date_to>')
def get_category_sales(date_from, date_to):
    data = utils.get_data()
    filtered_data = utils.filter_by_date_range(data, date_from, date_to)
    categories = {}
    total_sales = 0
    for d in filtered_data:
        for p in d['products']:
            if p['category'] in categories:
                categories[p['category']] += (p['price'] * p['quantity'])
                total_sales += (p['price'] * p['quantity'])
            else:
                categories[p['category']] = (p['price'] * p['quantity'])
                total_sales += (p['price'] * p['quantity'])
    for category in categories:
        categories[category] = (categories[category] / total_sales) * 100
    return jsonify(categories)
