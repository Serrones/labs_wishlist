from unittest import mock
from unittest.mock import Mock

import pytest

from src.products.client import get_product_by_id
from src.products.exceptions import ProductHttpException


class TestGetProductById:

    @pytest.fixture
    def valid_product(self):
        return {
            'price': 1699,
            'image': 'http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg',  # noqa
            'brand': 'bébé confort',
            'id:': '1bf0f365-fbdd-4e21-9786-da459d78dd1f',
            'title': 'Cadeira para Auto Iseos Bébé Confort Earth Brown'
        }

    def test_should_raise_http_exception(self):
        with pytest.raises(ProductHttpException):
            get_product_by_id('fake_id')

    def test_should_return_product_when_success(
        self,
        valid_product
    ):
        with mock.patch(
            'src.products.client.requests.get'
        ) as mock_get:

            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = valid_product

            response = get_product_by_id('fake_id')

            assert response == valid_product
