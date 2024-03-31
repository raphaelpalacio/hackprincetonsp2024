from django.contrib import admin

from .models import (AnalyzedImage, JsonLD, MetaTags, OpenGraph, SEOContent,
                     TwitterCard)

# Register your models here.


class JsonLDAdmin(admin.ModelAdmin):
    actions = ['regenerate_json_ld']

    def regenerate_json_ld(self, request, queryset):
        for obj in queryset:
            obj.generate()
        self.message_user(request, "JSON-LD regenerated for selected songs.")
    regenerate_json_ld.short_description = "Regenerate JSON-LD"


class MetaTagsAdmin(admin.ModelAdmin):
    actions = ['regenerate_meta_tags']

    def regenerate_meta_tags(self, request, queryset):
        for obj in queryset:
            obj.generate()
        self.message_user(request, "Meta Tags regenerated for selected songs.")
    regenerate_meta_tags.short_description = "Regenerate Meta Tags"


class OpenGraphAdmin(admin.ModelAdmin):
    actions = ['regenerate_open_graph']

    def regenerate_open_graph(self, request, queryset):
        for obj in queryset:
            obj.generate()
        self.message_user(
            request, "Open Graph tags regenerated for selected songs.")
    regenerate_open_graph.short_description = "Regenerate Open Graph tags"


class TwitterCardAdmin(admin.ModelAdmin):
    actions = ['regenerate_twitter_card']

    def regenerate_twitter_card(self, request, queryset):
        for obj in queryset:
            obj.generate()
        self.message_user(
            request, "Twitter Card tags regenerated for selected songs.")
    regenerate_twitter_card.short_description = "Regenerate Twitter Card tags"


class SEOContentAdmin(admin.ModelAdmin):
    actions = ['regenerate_seo_content']

    def regenerate_seo_content(self, request, queryset):
        for obj in queryset:
            obj.generate()
        self.message_user(
            request, "SEO Content regenerated for selected songs.")
    regenerate_seo_content.short_description = "Regenerate SEO Content"


class AnalyzedImageAdmin(admin.ModelAdmin):
    actions = ['regenerate_analyzed_image']

    def regenerate_analyzed_image(self, request, queryset):
        for obj in queryset:
            obj.generate()
        self.message_user(
            request, "Analyzed Image regenerated for selected songs.")
    regenerate_analyzed_image.short_description = "Regenerate Analyzed Image"


admin.site.register(JsonLD, JsonLDAdmin)
admin.site.register(MetaTags, MetaTagsAdmin)
admin.site.register(OpenGraph, OpenGraphAdmin)
admin.site.register(TwitterCard, TwitterCardAdmin)
admin.site.register(SEOContent, SEOContentAdmin)
admin.site.register(AnalyzedImage, AnalyzedImageAdmin)
