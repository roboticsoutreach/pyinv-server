from rest_framework import status
from rest_framework.exceptions import APIException


class UnableToDelete(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Unable to delete object because it is referenced by other objects.'
    default_code = 'protected_error'
