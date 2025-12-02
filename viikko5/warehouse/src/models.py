from . import db


class Warehouse(db.Model):
    __tablename__ = 'warehouses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    products = db.relationship(
        'Product', backref='warehouse', lazy=True, cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Warehouse {self.name}>'


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey('warehouses.id'), nullable=False
    )

    def __repr__(self):
        return f'<Product {self.name}>'
