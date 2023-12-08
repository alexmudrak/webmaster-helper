from django.contrib import admin

from seo_parser.models import SeoData


class SeoDataAdmin(admin.ModelAdmin):
    list_display = [
        "url",
        "type",
        "data",
        "created",
    ]


admin.site.register(SeoData, SeoDataAdmin)
