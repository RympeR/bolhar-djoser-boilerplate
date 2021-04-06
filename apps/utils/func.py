import os
import re
import random
import string
from django.core.validators import validate_email
from rest_framework import pagination
from rest_framework.response import Response


def set_phone(phone):
    if not phone:
        return None

    phone = str(phone)
    if phone and type(phone) is not int:
        phone = re.sub("\D", '', phone)

        # if phone[:1] == '0':
        #     phone = '38' + phone
        # if phone[:1] == '8':
        #     phone = '3' + phone
        #
        # if len(phone) == 12:
        return int(phone)
    return None


def set_email(email):
    try:
        validate_email(email)
        return email
    except Exception:
        return None


def id_generator(size=12, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def set_unique_file_name(file):
    if file:
        end_extension = file.rsplit('.', 1)[1]
        file_name = id_generator() + '.' + end_extension
        return file_name
    else:
        return None


def user_avatar(instance, filename):
    instance.original_file_name = filename
    file = set_unique_file_name(filename)
    return os.path.join('user', file)


def profession_image(instance, filename):
    instance.original_file_name = filename
    file = set_unique_file_name(filename)
    return os.path.join('profession', file)


def transform_get_value(value):
    if value == 'null':
        value = None
    elif value == 'true':
        value = True
    elif value == '1':
        value = True
    elif value == 'false':
        value = False
    elif value == '0':
        value = False
    elif value == '':
        value = None
    return value


class MyPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'results': data,
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
        })
