from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, ListField, FloatField, IntField, DateTimeField, EnumField
from datetime import datetime
from enum import Enum


class SizesEnum(Enum):
    XS = 'xs'
    SM = 'sm'
    MD = 'md'
    LG = 'lg'
    XL = 'xl'
    XXL = 'xxl'

class Sizes(EmbeddedDocument):
    size = EnumField(SizesEnum, required=True)
    quantity = IntField(min_value=0, required=True)

class Products(Document):
    name = StringField(regex=r'^[a-zA-Z0-9\s]+$', required=True, unique=True)
    price = FloatField(min_value=1.0, required=True)
    sizes = ListField(EmbeddedDocumentField(Sizes), required=True)
    total_quantity = IntField(min_value=0, required=True)
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())
    
    meta = {
        'collection': 'products',
    }