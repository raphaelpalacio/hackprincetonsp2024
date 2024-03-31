from django.contrib import admin

from .models import (JSON_LD, AnalyzedImage, MetaTags, OpenGraph, SEOContent,
                     TwitterCard)

# Register your models here.
admin.site.register(JSON_LD)
admin.site.register(AnalyzedImage)
admin.site.register(MetaTags)
admin.site.register(OpenGraph)
admin.site.register(SEOContent)
admin.site.register(TwitterCard)
