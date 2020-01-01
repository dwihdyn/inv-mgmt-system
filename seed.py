import os

os.environ['MIGRATION'] = '1'

if not os.getenv('FLASK_ENV') == 'production':
    print("Loading environment variables from .env")
    from dotenv import load_dotenv
    load_dotenv()

import peeweedbevolve
from models import *    # all import (*) being handled by __init__.py inside the 'models' folder  
import names

# =================================================================


# restart database
Store.delete().execute()
Warehouse.delete().execute()
Product.delete().execute()

# seeding store
i = 0
while i < 10:
    Store(name=names.get_full_name()).save()
    i = i + 1

# seeding warehouse
j = 1
while j < 11:
    Warehouse(location=names.get_full_name(), store=j).save()
    j = j + 1