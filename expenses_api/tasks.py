from __future__ import absolute_import, unicode_literals
from celery import shared_task

import random
import string

from .models import Category


# @shared_task
# def create_category():
#     category_name = ''.join([random.choice(string.ascii_letters) for i in range(5)])
#     new_object = Category.objects.create(name=category_name)
#     return new_object.name
