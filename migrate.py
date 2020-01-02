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
from models import db, Store, Warehouse, Product

print("Running Migration")
if os.getenv('FLASK_ENV') == 'production':
    db.evolve(ignore_tables={'base_model'}, interactive=False)
else:
    db.evolve(ignore_tables={'base_model'})
print("Finish Migration")




# =================== DELETE SEED FEATURE as it serves no purpose when app has launched to production ===================
# 

# ==========================SEEDING BELOW==========================
# TO BE IMPORVED USING SQLALCHEMY, as peewee is unable to do so




'''
import names


# restart database
Product().delete().execute()
Warehouse().delete().execute()
Store().delete().execute()


## restart store_id


# # better way is to reset true ID increment back to 1 https://stackoverflow.com/questions/5342440/reset-auto-increment-counter-in-postgres \d+ to see with hidden tables
# # resetting can be done using sqlalchemy https://kite.com/python/docs/sqlalchemy.orm.Session.execute https://stackoverflow.com/questions/36217535/initialize-sequence-after-deleting-table-sqlalchemy-postresql
# # below is sqlalchemy snippet
# db.session.execute("ALTER SEQUENCE test_id_seq RESTART WITH 1")
# db.session.commit()



# # seeding store
# i = 1
# while i < 11:
#     Store(name=names.get_full_name(), store_id=i).save(force_insert=True)
#     i = i + 1
# seed_store = True

# # seeding warehouse
# j = 1
# while j < 11:
#     Warehouse(location=names.get_full_name(), warehouse_id=j ,store=j).save(force_insert=True)
#     j = j + 1
# seed_warehouse = True


# seeding ALL
i = 1
while i < 11:
    Store(name=names.get_full_name(), store_id=i).save(force_insert=True) # force_insert used to make sure the new data ID starts with 1
    Warehouse(location=names.get_full_name(), warehouse_id=i ,store=i).save(force_insert=True)
    i = i + 1
seed_success = True




if seed_success:
    print('Seeding SUCCESS')
else:
    print('seeding FAILED. check migrate.py code while loop')
'''