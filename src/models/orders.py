from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, IntField, ListField, DateTimeField, ReferenceField
from datetime import datetime
from src.models.products import Products


class OrderItems(EmbeddedDocument):
    productId = ReferenceField(document_type=Products, required=True)
    quantity = IntField(min_value=1, required=True)

class Orders(Document):
    userId = IntField(required=True)
    items = ListField(EmbeddedDocumentField(OrderItems), required=True)
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())
    
    meta = {
        'collection': 'orders',
    }