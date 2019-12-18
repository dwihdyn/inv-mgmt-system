import peeweedbevolve
from flask import Flask, render_template, request, redirect, url_for
from models import db, Store, Warehouse, Product


app = Flask(__name__)

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

@app.route('/store/new', methods=['GET'])
def store_new():
    return render_template('store.html')


@app.route("/store/create", methods=['POST'])
def store_create():
    new_st = Store(name=request.args['new_store_name'])
    new_st.save()
    return redirect(url_for('index'))


@app.route("/stores", methods=['GET'])
def stores_list():
    # create column called 'num' to count how many warehouse is under the given store
    stores = Store.select()
    return render_template('stores.html', stores=stores)


if __name__ == "__main__":
    app.run()
