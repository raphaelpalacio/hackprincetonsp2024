from django.db import models

# Create your models here.
class opmodel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_all_names(cls):
        return list(cls.objects.values_list('name', flat=True))

    def optimize(self):
        
        raise NotImplementedError('You must implement the optimize method in your model')

