from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'C:\Program Files\DB Browser for SQLite\MyDatabase.db'
db = SQLAlchemy(app)

# Define the Product model
class Product(db.Model):
    product_id = db.Column(db.String(50), primary_key=True)

    def __repr__(self):
        return f"<Product {self.product_id}>"

# Define the Location model
class Location(db.Model):
    location_id = db.Column(db.String(50), primary_key=True)

    def __repr__(self):
        return f"<Location {self.location_id}>"

# Define the ProductMovement model
class ProductMovement(db.Model):
    movement_id = db.Column(db.String(50), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    from_location = db.Column(db.String(50), db.ForeignKey('location.location_id'))
    to_location = db.Column(db.String(50), db.ForeignKey('location.location_id'))
    product_id = db.Column(db.String(50), db.ForeignKey('product.product_id'))
    qty = db.Column(db.Integer)

    def __repr__(self):
        return f"<ProductMovement {self.movement_id}>"

# Create the database tables
db.create_all()

# Views
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        product = Product(product_id=product_id)
        db.session.add(product)
        db.session.commit()
        return redirect('/product/view/' + product_id)
    return render_template('add_prod.html')

@app.route('/product/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)
    if request.method == 'POST':
        product.product_id = request.form['product_id']
        db.session.commit()
        return redirect('/product/view/' + product.product_id)
    return render_template('edit_prod.html', product=product)

@app.route('/product/view/<product_id>')
def view_product(product_id):
    product = Product.query.get(product_id)
    return render_template('view_prod.html', product=product)

@app.route('/location/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        location_id = request.form['location_id']
        location = Location(location_id=location_id)
        db.session.add(location)
        db.session.commit()
        return redirect('/location/view/' + location_id)
    return render_template('add_loc.html')

@app.route('/location/edit/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get(location_id)
    if request.method == 'POST':
        location.location_id = request.form['location_id']
        db.session.commit()
        return redirect('/location/view/' + location.location_id)
    return render_template('edit_loc.html', location=location)

@app.route('/location/view/<location_id>')
def view_location(location_id):
    location = Location.query.get(location_id)
    return render_template('view_loc.html', location=location)

@app.route('/productmovement/add', methods=['GET', 'POST'])
def add_product_movement():
    if request.method == 'POST':
        timestamp = request.form['timestamp']
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        product_id = request.form['product_id']
        qty = int(request.form['qty'])

        movement = ProductMovement(timestamp=timestamp, from_location=from_location, to_location=to_location,
                                   product_id=product_id, qty=qty)
        db.session.add(movement)
        db.session.commit()
        return redirect('/productmovement/view/' + movement.movement_id)
    return render_template('addPro_movement.html')

@app.route('/productmovement/edit/<movement_id>', methods=['GET', 'POST'])
def edit_product_movement(movement_id):
    movement = ProductMovement.query.get(movement_id)
    if request.method == 'POST':
        movement.timestamp = request.form['timestamp']
        movement.from_location = request.form['from_location']
        movement.to_location = request.form['to_location']
        movement.product_id = request.form['product_id']
        movement.qty = int(request.form['qty'])
        db.session.commit()
        return redirect('/productmovement/view/' + movement.movement_id)
    return render_template('editPro_movement.html', movement=movement)

@app.route('/productmovement/view/<movement_id>')
def view_product_movement(movement_id):
    movement = ProductMovement.query.get(movement_id)
    return render_template('viewPro_movement.html', movement=movement)

@app.route('/report/balance')
def balance_report():
    locations = Location.query.all()
    products = Product.query.all()
    balance_data = []

    for product in products:
        for location in locations:
            qty = 0
            movements = ProductMovement.query.filter_by(product_id=product.product_id,
                                                        to_location=location.location_id).all()
            for movement in movements:
                qty += movement.qty
            movements = ProductMovement.query.filter_by(product_id=product.product_id,
                                                        from_location=location.location_id).all()
            for movement in movements:
                qty -= movement.qty
            balance_data.append({
                'product': product,
                'location': location,
                'qty': qty
            })

    return render_template('balance_report.html', balance_data=balance_data)

if __name__ == '__main__':
    app.run(debug=True)

