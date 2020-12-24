class ProductException(Exception):
    pass


class ProductHttpException(ProductException):
    def __init__(self, response):
        self.response = response
        super().__init__(
            'Failed Request. '
            f'Reason: {response.response.reason} '
            f'code: {response.response.status_code}'
        )
