"""
Product Service Routes
"""

from flask import request, abort
from service import app
from service.models import Product, Category
from service.common import status


######################################################################
# CREATE A PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """Create a Product"""
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    return product.serialize(), status.HTTP_201_CREATED


######################################################################
# LIST PRODUCTS (with filters)
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns all Products or filtered Products"""
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(Category[category])
    elif available:
        products = Product.find_by_availability(available.lower() == "true")
    else:
        products = Product.all()

    return [product.serialize() for product in products], status.HTTP_200_OK


######################################################################
# READ, UPDATE, DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["GET", "PUT", "DELETE"])
def product_by_id(product_id):
    """Retrieve, Update or Delete a Product"""
    app.logger.info("Request to process product with id [%s]", product_id)

    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Product with id '{product_id}' was not found."
        )

    # READ
    if request.method == "GET":
        return product.serialize(), status.HTTP_200_OK

    # UPDATE
    if request.method == "PUT":
        product.deserialize(request.get_json())
        product.id = product_id
        product.update()
        return product.serialize(), status.HTTP_200_OK

    # DELETE
    if request.method == "DELETE":
        product.delete()
        return "", status.HTTP_204_NO_CONTENT
