# `flask run` to deploy

import peeweedbevolve
from flask import Flask, render_template, request, redirect, url_for
from models import db, Store, Warehouse, Product


app = Flask(__name__)

# database setup
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


# === website directory ===
@app.route('/')
def index():
    store_name = request.args.get('store_name')
    return render_template("index.html", store_name=store_name)


# take user to enter store name
@app.route('/store/new')
def store():
    return render_template('store.html')


# once user type new store name & press submit, go here (backend setup)
@app.route("/store/create")
def store_create():
    # request.args() for one input |  request.form() for whole form info name, address, etc
    new_st = Store(name=request.args['new_store_name'])
    new_st.save()
    return redirect(url_for('index'))


@app.route("/all-stores")
def show_store_list():
    all_store = Store.select()
    return render_template('all-store.html', all_store=all_store)


if __name__ == "__main__":
    app.run()
