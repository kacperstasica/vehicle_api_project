from rest_framework.exceptions import APIException


class CarException(APIException):
    status_code = 503
    default_detail = 'Such car does not exist in our database, try again with another make or model.'
    default_code = 'service_unavailable'


class ReviewException(APIException):
    status_code = 503
    default_detail = 'No car with given id. Please Try again with another id.'
    default_code = 'service_unavailable'
