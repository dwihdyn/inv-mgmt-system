'''
since migrate.py & seed.py combined, you have to 
    `dropdb inv_mgmt_flask_demo`
    `createdb inv_mgmt_flask_demo`
    `python migrate.py`

in order to reset the ID counter, since product depend on warehouse ID & warehouse depend on store ID
'''

import os

os.environ['MIGRATION'] = '1'

if not os.getenv('FLASK_ENV') == 'production':
    print("Loading environment variables from .env")
    from dotenv import load_dotenv
    load_dotenv()


import peeweedbevolve
from models import *

print("Running Migration")
if os.getenv('FLASK_ENV') == 'production':
    db.evolve(ignore_tables={'base_model'}, interactive=False)
else:
    db.evolve(ignore_tables={'base_model'})
print("Finish Migration")



# ==========================SEEDIND BELOW==========================


import names



# restart database
Product().delete().execute()
Warehouse().delete().execute()
Store().delete().execute()

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