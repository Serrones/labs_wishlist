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

    def test_verify_user_repr(
        self,
        user
    ):
        assert user.__repr__() == '<User fake>'

    def test_verify_password(
        self,
        user
    ):
        assert user.check_password('fake_password')
        assert not user.check_password('just_fake')

    def test_as_dict_should_return_username_and_email(
        self,
        user
    ):
        user_dict = user.as_dict()

        assert user_dict['username'] == 'fake'
        assert user_dict['email'] == 'fake@email.com'


class TestProduct:

    @pytest.fixture
    def product(self):
        return Product(
            product_id='fake_product_id'
        )

    def test_verify_product_repr(
        self,
        product
    ):
        assert product.__repr__() == '<Product fake_product_id>'
