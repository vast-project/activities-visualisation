from django.db import models

# https://medium.com/django-rest-framework/django-rest-framework-viewset-when-you-don-t-have-a-model-335a0490ba6f
class SparqlQuery(object):
    def __init__(self, **kwargs):
        for field in ('q'):
            setattr(self, field, kwargs.get(field, None))
