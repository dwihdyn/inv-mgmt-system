import os
import peeweedbevolve
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Store, Warehouse, Product
from peewee import fn, JOIN


app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

# for migrate.py, `flask migrate` to run
@app.cli.command(short_help='Migrate Database')
def migrate():
    db.evolve(ignore_tables={'base_model'})



@app.route('/')
def index():
    return render_template("index.html")


# ====================== STORE ======================

# create
@app.route('/store/new', methods=['GET'])
def store_new():
    return render_template('store.html')

@app.route("/store/create", methods=['POST'])
def store_create():
    new_st = Store(name=request.form['name'])
    
    if not Store.get_or_none(Store.name == new_st.name):
        if new_st.save():
            flash("New store successfully created!", "success")
            return redirect(url_for('stores_list'))
        else:
            flash("Something went wrong, please check your internet and try again", "danger")
            return render_template('store.html', name=request.form['name'])
    else:
        flash("Store has already existed", "danger")
        return render_template('store.html', name=request.form['name'])


# read
@app.route("/stores", methods=['GET'])
def stores_list():
    # create column called 'num' to count how many warehouse is under the given store
    stores = Store.select(Store.name, Store.store_id, fn.COUNT(Warehouse.store_id).alias('count')
    ).join(Warehouse, JOIN.LEFT_OUTER
    ).group_by(Store.store_id
    ).order_by(Store.name)
    return render_template('stores.html', stores=stores)


# delete
@app.route("/store/<int:id>/delete", methods=['POST'])
def store_delete(id):
    del_st = Store.get_by_id(id)
    wh_checking = Warehouse.get_or_none(Warehouse.store_id == del_st)

    if wh_checking:
        wh_checking.delete().where(Warehouse.store_id == wh_checking.store_id).execute()

    if del_st.delete_instance():
        flash('Successfully deleted!', 'success')
    else:
        flash('Something went wrong, check your internet and try again', 'danger')
    
    return redirect(url_for('stores_list'))


# update
@app.route('/store/<int:id>', methods=['GET'])
def store_show(id):
    sel_st = Store.get_by_id(id)
    return render_template('store_show.html', sel_st=sel_st)

@app.route('/store/<int:id>/update', methods=['POST'])
def store_update(id):
    # not getting the id will lead to creating new data
    updated_st = Store(store_id=id, name=request.form['name'])
    if updated_st.save(only=[Store.name]):
        flash("Successfully updated!", 'success')
    else:
        flash("Something went wrong, check your internet and try again", 'danger')

    return redirect(url_for('store_show', id=id)) # return back to store_show.html with the selected store_id


# ====================== WAREHOUSE ======================

# create
@app.route('/warehouse/new', methods=['GET'])
def warehouse_new():
    stores = Store.select()
    return render_template('warehouse.html', stores=stores)


@app.route('/warehouse/create', methods=['POST'])
def warehouse_create():
    connected_st = Store.get_or_none(Store.store_id == request.form['store_id'])

    if not connected_st:
        flash('Selected store does not exist, please create a store first', 'danger')
        return redirect(url_for('warehouse_new'))

    new_wh = Warehouse(location=request.form['location'], store=connected_st)

    if new_wh.save():
        flash('Warehouse Successfully created!', "success")
        return redirect(url_for('warehouses_list'))
    else:
        flash('Please check your internet connection and try again', 'danger')
        return render_template('warehouse.html')




# read
@app.route('/warehouses', methods=['GET'])
def warehouses_list():
    warehouses = Warehouse.select(Warehouse.location, Warehouse.warehouse_id, Warehouse.store ,  fn.COUNT(Product.warehouse_id).alias('count')
    ).join(Product, JOIN.LEFT_OUTER
    ).group_by(Warehouse.warehouse_id
    ).order_by(Warehouse.location)
    # warehouses = Warehouse.select()
    return render_template('warehouses.html', warehouses = warehouses)



# delete
@app.route('/warehouse/<int:id>/delete', methods=['POST'])
def warehouse_delete(id):
    del_wh = Warehouse.get_by_id(id)
    prod_checking = Product.get_or_none(Product.warehouse_id == del_wh)

    if prod_checking:
        prod_checking.delete().where(Product.warehouse_id == prod_checking.warehouse_id).execute()
    
    if del_wh.delete_instance():
        flash('Successfully deleted!', 'success')
    else:
        flash('Something went wrong, check your internet and try again', 'danger')

    return redirect(url_for('warehouses_list'))


# update
@app.route('/warehouse/<int:id>', methods=['GET'])
def warehouse_show(id):
    sel_wh = Warehouse.get_by_id(id)
    return render_template('warehouse_show.html', sel_wh=sel_wh)

@app.route('/warehouse/<int:id>/update', methods=['POST'])
def warehouse_update(id):
    updated_wh = Warehouse(warehouse_id=id, location=request.form['location'])
    if updated_wh.save(only=[Warehouse.location]):
        flash("Successfully updated!", 'success')
    else:
        flash("Something went wrong, check your internet and try again", 'danger')
    return redirect(url_for('warehouse_show', id=id))




# ====================== PRODUCT ======================


# create
@app.route('/product/new', methods=['GET'])
def product_new():
    warehouses = Warehouse.select()
    return render_template('product.html', warehouses=warehouses)


@app.route('/product/create', methods=['POST'])
def product_create():
    
    connected_wh = Warehouse.get_or_none(Warehouse.warehouse_id == request.form['warehouse_id'])

    if not connected_wh:
        flash('Selected warehouse does not exist, please create a warehouse first', 'danger')
        return redirect(url_for('product_new'))

    new_prod = Product(name=request.form['name'], description=request.form['description'], color=request.form['color'], warehouse=connected_wh)

    if new_prod.save():
        flash('Product Successfully created!', "success")
        return redirect(url_for('products_list'))
    else:
        flash('Please check your internet connection and try again', 'danger')
        return render_template('product.html')



# read
@app.route('/products', methods=['GET'])
def products_list():
    products = Product.select()
    return render_template('products.html', products = products)




# delete
@app.route('/product/<int:id>/delete', methods=['POST'])
def product_delete(id):
    del_prod = Product.get_by_id(id)
    
    if del_prod.delete_instance():
        flash('Successfully deleted!', 'success')
    else:
        flash('Something went wrong, check your internet and try again', 'danger')

    return redirect(url_for('products_list'))


# update
@app.route('/product/<int:id>', methods=['GET'])
def product_show(id):
    sel_prod = Product.get_by_id(id)
    return render_template('product_show.html', sel_prod=sel_prod)

@app.route('/product/<int:id>/update', methods=['POST'])
def product_update(id):
    updated_prod = Product(product_id=id, name=request.form['name'])
    if updated_prod.save(only=[Product.name]):
        flash("Successfully updated!", 'success')
    else:
        flash("Something went wrong, check your internet and try again", 'danger')
    return redirect(url_for('product_show', id=id))






if __name__ == "__main__":
    app.run()
