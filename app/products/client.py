import logging

import requests
from requests import HTTPError

from app.products.exceptions import ProductHttpException

PRODUCTS_URL = 'http://challenge-api.luizalabs.com/api/product'


def get_product_by_id(id: str) -> dict:
    product_url = f'{PRODUCTS_URL}/{id}/'

    try:
        response = requests.get(product_url)
        response.raise_for_status()

        product = response.json()
        logging.info(
            f'Fetching product with id {id}'
        )
        return product

    except HTTPError as exc:
        logging.warning(
            f'Failed to fetch product with id {id}'
        )
        raise ProductHttpException(exc)
