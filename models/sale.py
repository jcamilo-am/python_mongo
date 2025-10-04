from bson import ObjectId

class Sale:
    def __init__(self, db):
        self.collection = db['ventas']  # supermarket collection name

    def get_all(self):
        """Get all sales from database"""
        sales = list(self.collection.find())

        # Convert ObjectId to string for JSON serialization
        for s in sales:
            if '_id' in s:
                s['_id'] = str(s['_id'])

        return sales

    def get_sales_report(self):
        """Run the provided aggregation pipeline and return the result"""
        pipeline = [
            { "$unwind": "$items" },
            {
                "$lookup": {
                    "from": "productos",
                    "localField": "items.producto_id",
                    "foreignField": "_id",
                    "as": "producto"
                }
            },
            { "$unwind": "$producto" },
            {
                "$group": {
                    "_id": "$_id",
                    "cliente_id": { "$first": "$cliente_id" },
                    "fecha": { "$first": "$fecha" },
                    "total": { "$first": "$total" },
                    "productos": {
                        "$push": {
                            "nombre": "$producto.nombre",
                            "precio": "$producto.precio",
                            "cantidad": "$items.cantidad"
                        }
                    }
                }
            },
            {
                "$project": {
                    "cliente_id": 1,
                    "fecha": 1,
                    "total": 1,
                    "productos": 1
                }
            }
        ]

        result = list(self.collection.aggregate(pipeline))
        return result
