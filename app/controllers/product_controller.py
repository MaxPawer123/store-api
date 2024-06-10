from flask import Blueprint, request, jsonify
from app.models.product_model import Product
from app.views.product_view import render_product_detail, render_product_list
from app.utils.decorators import jwt_required, roles_required
#Crear un blueprint para el controlador
product_bp = Blueprint("product", __name__)


#crear por partes
#Ruta para obtener la lista de productos
@product_bp.route("/products", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_products():
    products = Product.get_all()
    return jsonify(render_product_list(products))


#Ruta para obtener un producto especifico por id 
@product_bp.route("/products/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_product(id):
    product = Product.get_by_id(id)
    if product:
        return jsonify(render_product_detail(product))
    return jsonify({"error":"Producto no encontrado"}), 404

#Ruta para crear un nuevo producto y guardarlo en la base de datos
@product_bp.route("/products", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_product():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock")

    #Validadcion simple de datos de entrada
    if not name or not description or not price or not stock:
        return jsonify({"error":"Faltan datos requeridos"}), 400
   
    #Crear un nuevo producto
    product = Product(name=name, description=description, price=price, stock=stock)
    product.save()
    return jsonify(render_product_detail(product)), 201


#Ruta para actualizar un producto existente
@product_bp.route("/products/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_product(id):
    product = Product.get_by_id(id)
    if not product:
        return jsonify({"error":"Producto no encontrado"}), 404
    
    data = request.json
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock")

    #Actualziar los datos del producto
    product.update(name=name, description=description, price=price, stock=stock)
    return jsonify(render_product_detail(product))

#Ruta para eliminar un producto existente
@product_bp.route("/products/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_product(id):
    product = Product.get_by_id(id)
    if not product:
        return jsonify({"error":"producto no encontrado"}),404
    
    #eliminar el producto de la base de datos
    product.delete()
    
    #Respuesta vacia con codigo de estado 204
    return "", 204

