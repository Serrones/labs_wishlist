from unittest import mock
from unittest.mock import Mock

import pytest

from app.products.client import get_product_by_id
from app.products.exceptions import ProductHttpException


class TestGetProductById:

    def test_should_raise_http_exception(self):
        with pytest.raises(ProductHttpException):
            get_product_by_id('fake_id')

    def test_should_return_product_when_success(
        self,
        valid_product
    ):
        with mock.patch(
            'app.products.client.requests.get'
        ) as mock_get:

            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = valid_product

            response = get_product_by_id('fake_id')

            assert response == valid_product
