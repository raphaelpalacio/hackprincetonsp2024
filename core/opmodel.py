from django.db import models
from pyld import jsonld
from django.core.serializers import serialize,DjangoJSONEncoder
import json

# Create your models here.
class opmodel(models.Model):
    class Meta:
        abstract = True

    # when it initializes the model, it will create the object
    def __init__(self, *args, **kwargs):
        super(opmodel, self).__init__(*args, **kwargs) # after initializing the model, it will convert the object to jsonld
        self.jsonld = jsonld(self)
        print(self.jsonld)

    @classmethod
    def get_all_names(cls):
        return list(cls.objects.values_list('name', flat=True))

# define a class named jsonld which could init the object and convert the django model instance to jsonld
class jsonld():
    def __init__(self, model_instance):
        self.data = self.convert_to_jsonld(model_instance)

    def convert_to_jsonld(self, model_instance):
        # Example implementation: Convert Django model instance to JSON
        data = model_instance.__dict__  # Get dictionary representation of model instance
        # Optionally, you can manipulate the data or add JSON-LD specific keys like "@context", "@type", etc.
        # For demonstration purposes, let's add a context and type
        data["@context"] = "https://schema.org"
        data["@type"] = model_instance.__class__.__name__  # Assuming class name corresponds to JSON-LD type
        return data

    def to_json(self):
        return json.dumps(self.data, cls=DjangoJSONEncoder)

    @classmethod
    def from_json(cls, json_data):
        return cls(json.loads(json_data))





