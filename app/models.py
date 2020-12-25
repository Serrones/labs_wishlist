from typing import Any

from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class Product(db.Model):  # type: ignore
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(36), index=True)
    price = db.Column(db.Float)
    image = db.Column(db.String(120))
    brand = db.Column(db.String(60))
    title = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Product {self.product_id}>'

    def as_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'price': self.price,
            'image': self.image,
            'brand': self.brand,
            'title': self.title
        }

    def from_dict(self, data):
        for field in ['price', 'image', 'brand', 'title']:
            setattr(self, field, data[field])


class User(db.Model):  # type: ignore
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    products = db.relationship(
        'Product',
        backref='user',
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password: Any) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: Any) -> bool:
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'products': [product.as_dict() for product in self.products]
        }

    def from_dict(self, data):
        for field in ['username', 'email', 'is_admin']:
            if field in data:
                setattr(self, field, data[field])
