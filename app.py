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
@app.cli.command()
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

    return redirect(url_for('store_show', id=id))


# ====================== WAREHOUSE ======================

# create
@app.route('/warehouse/new', methods=['GET'])
def warehouse_new():
    stores = Store.select()
    return render_template('warehouse.html', stores=stores)


@app.route('/warehouse/create', methods=['POST'])
def warehouse_create():
    connected_st = Store.get_or_none(Store.store_id == request.form['store_id'])
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
    warehouses = Warehouse.select()
    return render_template('warehouses.html', warehouses = warehouses)

# delete

# update



if __name__ == "__main__":
    app.run()
