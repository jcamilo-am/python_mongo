from flask import Flask, jsonify
from pymongo import MongoClient
from routes.tasks import tasks_bp, init_task_model
from routes.sales import sales_bp, init_sale_model
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'tareas')
SUPERMARKET_DB_NAME = os.getenv('SUPERMARKET_DB', 'supermarket')
PORT = int(os.getenv('PORT', '5000'))

app = Flask(__name__)

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Agregar base de datos del supermercado
db_supermarket = client[SUPERMARKET_DB_NAME]


init_task_model(db)
init_sale_model(db_supermarket)

# Register blueprints
app.register_blueprint(tasks_bp)
app.register_blueprint(sales_bp)

@app.route('/')
def index():
    collections = db.list_collection_names()
    
    return jsonify({
        'database': DATABASE_NAME,
        'collections': collections,
        'routes': [
            '/',
            '/api/tasks/',
            '/api/sales/'
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)