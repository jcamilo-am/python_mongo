from flask import Blueprint, jsonify
from models.sale import Sale

sales_bp = Blueprint('sales', __name__, url_prefix='/api/sales')

sale_model = None

def init_sale_model(db):
    global sale_model
    sale_model = Sale(db)

@sales_bp.route('/', methods=['GET'])
def get_all_sales():
    try:
        sales = sale_model.get_all()
        return jsonify({
            'success': True,
            'count': len(sales),
            'sales': sales
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error fetching sales'
        }), 500

@sales_bp.route('/report', methods=['GET'])
def get_sales_report():
    try:
        report = sale_model.get_sales_report()
        return jsonify({
            'success': True,
            'count': len(report),
            'report': report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error generating sales report'
        }), 500
