from flask import Blueprint, render_template, request, redirect
from models.product_model import Product

product_controller = Blueprint("product_controller", __name__)

products = []

@product_controller.route("/", methods=["GET"])
def product_index():
  products_dict = [product.to_dict() for product in products]
  return render_template("products.html", products=products_dict)


@product_controller.route("/add", methods=["GET", "POST"])
def add_new_product():
  if request.method == "POST":
    id = int(request.form.get("id"))
    name = request.form.get("name")
    price = float(request.form.get("price"))

    products.append(Product(id, name, price))
    
    return redirect("/products")
  
  return render_template("add_product.html")