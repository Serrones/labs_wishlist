import pytest

from app.models import Product, User


class TestUser:

    @pytest.fixture
    def user(self):
        user = User(
            username='fake',
            email='fake@email.com',
        )
        user.set_password('fake_password')
        return user

    def test_verify_user_repr(self, user):
        assert user.__repr__() == '<User fake>'

    def test_verify_user_as_dict(self, user):

        user_dict = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
            'products': [product.as_dict() for product in user.products]
        }
        assert user.as_dict() == user_dict

    def test_verify_user_from_dict(self):

        user_dict = {
            'username': 'fake_user',
            'email': 'fake_user@email',
            'is_admin': False
        }
        user = User()
        user.from_dict(user_dict)

        assert user.username == user_dict['username']
        assert user.email == user_dict['email']
        assert user.is_admin == user_dict['is_admin']

    def test_verify_password(self, user):
        assert user.check_password('fake_password')
        assert not user.check_password('just_fake')


class TestProduct:

    @pytest.fixture
    def product(self):
        return Product(
            product_id='fake_product_id'
        )

    def test_verify_product_repr(self, product):
        assert product.__repr__() == '<Product fake_product_id>'

    def test_verify_product_as_dict(self, product):

        product_dict = {
            'id': product.id,
            'product_id': product.product_id,
            'price': product.price,
            'image': product.image,
            'brand': product.brand,
            'title': product.title
        }
        assert product.as_dict() == product_dict
