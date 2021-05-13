from rest_framework import status
from rest_framework.exceptions import APIException


class Api202(APIException):
    status_code = status.HTTP_202_ACCEPTED
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field):
        if detail is not None:
            self.detail = {field: detail}
        else:
            self.detail = {'detail': [self.default_detail]}


class Api400(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field):
        if detail is not None:
            self.detail = {field: detail}
        else:
            self.detail = {'detail': [self.default_detail]}
