from flask import Flask, render_template, request, redirect
import random
import datetime
app = Flask(__name__)

cart = []
orders = {}

products = [
    {"id": 1, 
     "name": "Laptop",
       "price": 50000, 
       "category": "Electronics",
     "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400",
     "reviews": []},

    {"id": 2, 
     "name": "Headphones", 
     "price": 2000, 
     "category": "Electronics",
     "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
     "reviews": []},


    {"id": 3, 
     "name": "T-Shirt", 
     "price": 999,
    "category": "Clothing",
    
     "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
     "reviews": []},

    {"id": 4,
      "name": "Shoes", 
      "price": 2500, 
      "category": "Clothing",
      
     "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
     "reviews": []},

    {"id": 5, 
     "name": "Smartphone", 
     "price": 30000,
    "category": "Electronics",
     "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400",
     "reviews": []},

    {"id": 6, 
     "name": "Smart Watch",
       "price": 7000,
     "category": "Electronics",
     "image": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400",
     "reviews": []},

    {"id": 7,
      "name": "Jeans", 
      "price": 1999,
    "category": "Clothing",
    
    
     "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400",
     "reviews": []},

    {"id": 8, 
     "name": "Jacket", 
     "price": 3500, 
     "category": "Clothing",
     
     "image": "https://images.unsplash.com/photo-1520975916090-3105956dac38?w=400",
     "reviews": []},
     {
    "id": 9,
    "name": "Bluetooth Speaker",
    "price": 3500,
    "category": "Electronics",
    "image": "https://images.unsplash.com/photo-1589003077984-894e133dabab",
    "reviews": []
},
{
    "id": 11,
    "name": "Hoodie",
    "price": 1999,
    "category": "Clothing",
   
    "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=400&q=60",
    "reviews": []
},
{
    "id": 12,
    "name": "Backpack",
    "price": 2200,
    "category": "Clothing",
    "image": "https://images.unsplash.com/photo-1509762774605-f07235a08f1f",
    "reviews": []
},

]


@app.route('/')
def home():
    return render_template("index.html", products=products)

@app.route('/add_review/<int:product_id>', methods=['POST'])
def add_review(product_id):
    name = request.form.get("name")
    review = request.form.get("review")
    rating = request.form.get("rating")

    for product in products:
        if product["id"] == product_id:
            product["reviews"].append({
                "name": name,
                "review": review,
                "rating": rating
            })

    return redirect('/')

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get("quantity", 1))

    for product in products:
        if product["id"] == product_id:
            cart.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity
            })
            break

    return redirect('/')
@app.route('/cart')
def view_cart():
    total = sum(item["price"] * item.get("quantity", 1) for item in cart)
    return render_template("cart.html", cart=cart, total=total)
@app.route('/remove_from_cart/<int:index>')
def remove_from_cart(index):
    if 0 <= index < len(cart):
        cart.pop(index)
    return redirect('/cart')
@app.route('/update_quantity/<int:index>', methods=['POST'])
def update_quantity(index):

    quantity = int(request.form.get("quantity", 1))

    if 0 <= index < len(cart):
        cart[index]["quantity"] = quantity

    return redirect('/cart' )

@app.route('/payment')
def payment():
    if not cart:
        return redirect('/cart')

    total = sum(item["price"] * item["quantity"] for item in cart)
    return render_template("payment.html", total=total)


@app.route('/place_order')
def place_order():
    if not cart:
        return redirect('/cart')

    order_id = random.randint(1000, 9999)

    orders[order_id] = {
        "items": cart.copy(),
        "status": "Order Placed",
        "placed_time": datetime.datetime.now(),
        "shipped_time": None,
        "delivered_time": None
    }

    cart.clear()

    return render_template("order_success.html", order_id=order_id)

@app.route('/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        order_id = int(request.form.get("order_id"))
        order = orders.get(order_id)

        if order:
            # Calculate time difference
            elapsed = (datetime.datetime.now() - order["placed_time"]).seconds

            if elapsed > 20:
                order["status"] = "Delivered"
            elif elapsed > 10:
                order["status"] = "Shipped"
            else:
                order["status"] = "Order Placed"

            return render_template(
                "track_result.html",
                order_id=order_id,
                order=order
            )
        else:
            return render_template("track_result.html", order_id=None)

    return render_template("track.html")

@app.route('/get_status/<int:order_id>')
def get_status(order_id):
    order = orders.get(order_id)

    if order:
        elapsed = (datetime.datetime.now() - order["placed_time"]).seconds

        if elapsed > 20:
            order["status"] = "Delivered"
        elif elapsed > 10:
            order["status"] = "Shipped"
        else:
            order["status"] = "Order Placed"

        return {"status": order["status"]}

    return {"status": "Invalid"}
    return redirect('/track')
   
if __name__ == '__main__':
    app.run(debug=True)
