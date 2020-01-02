import os
import peewee as pw
import datetime
from database import db


class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    updated_at = pw.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        database = db
        # False is to set our db table names in snake convention (base_model). if true (default), naming will be no convention (basemodel) hence ignore_tables wont be able to detect, and basemodel WONT be ignored.
        legacy_table_names = False


class Store(BaseModel):
    store_id = pw.AutoField()
    name = pw.CharField(unique=True)


class Warehouse(BaseModel):
    warehouse_id = pw.AutoField()
    location = pw.TextField()
    store = pw.ForeignKeyField(Store, backref='sel_wh')


class Product(BaseModel):
    product_id = pw.AutoField()
    name = pw.CharField(index=True)
    description = pw.TextField(null=True)
    color = pw.CharField(null=True)
    warehouse = pw.ForeignKeyField(Warehouse, backref='sel_prod')
