from app.database import db

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    #Iniciar la clase 'Product'
    def __init__(self, name, description, price, stock):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

    #Guardar un producto en la base de datos
    def save(self):
        db.session.add(self)
        db.session.commit()

    #Obtener todos los productos de la base de datos
    @staticmethod
    def get_all():
        return Product.query.all()

    #Obtener un producto por su id
    @staticmethod
    def get_by_id(id):
        return Product.query.get(id)
    #Actualizar un producto
    def update(self, name=None, description=None, price=None, stock=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if price is not None:
            self.price = price
        if stock is not None:
            self.stock = stock

        db.session.commit()

    #Eliminar un producto
    def delete(self):
        db.session.delete(self)
        db.session.commit()