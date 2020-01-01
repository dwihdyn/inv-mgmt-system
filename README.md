## Inventory Management System

### Database structure

```
stores
  |_ warehouses
       |_ products
```

#### Step by step to clone this project

```
Markup : 0. Git clone & install conda, and `conda create -n inv-mgmt python=3.7 anaconda` and `conda activate inv-mgmt` env creation
         1. `pip install -r requirements.txt` install required packages
         2. `createdb inv-mgmt` create psql database foundation
         3. `flask migrate` create our databases
         4. `python seed.py`  populate our database
         5. `flask run` deploy app
```
