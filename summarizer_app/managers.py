from django.db import models
from django.utils.crypto import get_random_string


class SummarizationManager(models.Manager):
    def create(self, **obj_data):

        obj_data['summary_id'] = get_random_string(8)

        return super().create(**obj_data)
