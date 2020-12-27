class ProductException(Exception):
    pass


class ProductHttpException(ProductException):
    def __init__(self, response):
        self.response = response
        self.reason = response.response.reason
        self.code = response.response.status_code
        super().__init__(
            'Failed Request. '
            f'Reason: {response.response.reason} '
            f'code: {response.response.status_code}'
        )
