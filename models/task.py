from bson import ObjectId

class Task:
    def __init__(self, db, supermarket_db=None):
        self.collection = db['tarea']  # existing primary collection
        self.db = db
        self.supermarket_db = supermarket_db  # optional second DB handle
    
    def get_all(self):
        """Get all tasks from database"""
        tasks = list(self.collection.find())
        
        # Convert ObjectId to string for JSON serialization
        for task in tasks:
            if '_id' in task:
                task['_id'] = str(task['_id'])
        
        return tasks

    def list_supermarket_collections(self):
        """Helper: list collections in the supermarket DB (if connected)"""
        if not self.supermarket_db:
            return []
        return self.supermarket_db.list_collection_names()

    # New: complex report pipeline
    def get_task_report(self):
        pipeline = [
            {
                "$lookup": {
                    "from": "estado_tarea",
                    "localField": "id_estado_tarea",
                    "foreignField": "_id",
                    "as": "estado_info"
                }
            },
            {
                "$lookup": {
                    "from": "proyecto",
                    "localField": "id_proyecto",
                    "foreignField": "_id",
                    "as": "proyecto_info"
                }
            },
            {
                "$lookup": {
                    "from": "responsable",
                    "localField": "id_responsable",
                    "foreignField": "_id",
                    "as": "responsable_info"
                }
            },
            { "$unwind": "$estado_info" },
            { "$unwind": "$proyecto_info" },
            { "$unwind": "$responsable_info" },
            {
                "$addFields": {
                    "grupo_etareo": {
                        "$switch": {
                            "branches": [
                                {
                                    "case": {
                                        "$and": [
                                            {"$gt": ["$responsable_info.edad", 17]},
                                            {"$lte": ["$responsable_info.edad", 30]}
                                        ]
                                    },
                                    "then": "adulto joven"
                                },
                                {
                                    "case": {
                                        "$and": [
                                            {"$gt": ["$responsable_info.edad", 30]},
                                            {"$lte": ["$responsable_info.edad", 50]}
                                        ]
                                    },
                                    "then": "adulto medio"
                                },
                                {
                                    "case": {"$gt": ["$responsable_info.edad", 50]},
                                    "then": "adulto mayor"
                                }
                            ],
                            "default": "sin clasificar"
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "nombre_tarea": 1,
                    "estado_tarea": "$estado_info.estado_tarea",
                    "nombre_proyecto": "$proyecto_info.nombre_proyecto",
                    "nombre_responsable": "$responsable_info.nombre_responsable",
                    "apellido_responsable": "$responsable_info.apellido_responsable",
                    "edad": "$responsable_info.edad",
                    "grupo_etareo": 1
                }
            },
            {
                "$sort": {
                    "nombre_responsable": 1
                }
            }
        ]

        # Ejecutar pipeline y devolver resultado
        result = list(self.collection.aggregate(pipeline))
        return result