from flask import Blueprint, jsonify
from models.task import Task

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

# Global variable for task model
task_model = None

def init_task_model(db):
    """Initialize task model with database connection"""
    global task_model
    task_model = Task(db)

@tasks_bp.route('/', methods=['GET'])
def get_all_tasks():
    """Get all tasks from database"""
    try:
        tasks = task_model.get_all()
        return jsonify({
            'success': True,
            'count': len(tasks),
            'tasks': tasks
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error fetching tasks'
        }), 500

# New: report route
@tasks_bp.route('/report', methods=['GET'])
def get_task_report():
    """Get complex task report with joins and calculations"""
    try:
        report = task_model.get_task_report()
        return jsonify({
            'success': True,
            'count': len(report),
            'report': report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error generating task report'
        }), 500
