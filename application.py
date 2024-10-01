# Import
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

application = Flask(__name__)
application.config['SECRET_KEY'] = 'A04b23d21a24'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(application)
login_manager.init_app(application)
login_manager.login_view = 'login'
CORS(application)

# module
# user (id,username, password)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=True)
    cart = db.relationship('CartItem', backref='user', lazy=True)
    
# Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
 
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
     
 
# autentication
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@application.route('/')
def initial():
    return 'API up!'

@application.route('/login', methods=['POST'])
def login():
    data = request.json
    
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and data.get('password') == user.password:
            login_user(user)        
            return jsonify({'message': "Logged in successfully"})
        
    return jsonify({'message': "Unauthorized. Invalid credentials"}), 401
@application.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': "Logout successfully"})

@application.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price':
        product = Product(name=data['name'],price=data['price'],description=data.get('description', ''))
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': "Product Registered successfully"})
    return jsonify({'message': "Invalid product data"}), 400

@application.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    #Retrieve the product from the database
    #Check if product exists
    #if exists, delete from database
    #if doesn't exists, return 404 not found
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': "Product Deleted successfully"})
    return jsonify({'message': "Product not found"}), 404

@application.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description
        })
    return jsonify({"message": "product not found"}), 404

@application.route('/api/products/update/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    data = request.json
    if 'name' in data:
        product.name = data['name']
        
    if 'price' in data:
        product.price = data['price']
        
    if 'description' in data:
        product.description = data['description']
    
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@application.route('/api/products', methods=["GET"])
def get_products():
    products = Product.query.all()
    print(products)
    product_list = []
    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
        }
        product_list.append(product_data)
        
    return jsonify(product_list)

# Checkout
@application.route('/api/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    # User
    user = User.query.get(int(current_user.id))
    # Product
    product = Product.query.get(product_id)
    
    if user and product:
        cart_item = CartItem(user_id=user.id, product_id=product.id)
        db.session.add(cart_item)
        db.session.commit()
        
        return jsonify({'message': 'Item added to the cart successfully'})
    return jsonify({'message': 'Failed to add item to the cart'}), 400
    
@application.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    # Product, User = Cart Item
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item removed from the cart successfully'})
    return jsonify({'message': 'Failed to remove item from the cart'}), 400

@application.route('/api/cart', methods=['GET'])
@login_required
def view_cart():
    # User
    user = User.query.get(int(current_user.id))
    cart_items = user.cart
    cart_content = []
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        cart_content.append(  {
                                "Product_price": product.price,
                                "product_name": product.name,
                                "id": cart_item.id,
                                "user_id": cart_item.user_id,
                                "product_id": cart_item.product_id
                                })
    return jsonify(cart_content)

@application.route('/api/cart/checkout', methods=['POST'])
@login_required
def checkout():
    user = User.query.get(current_user.id)
    cart_items = user.cart
    for cart_item in cart_items:
         db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Checkout successfully'})
         

if __name__ == "__main__":
    application.run(debug=True)