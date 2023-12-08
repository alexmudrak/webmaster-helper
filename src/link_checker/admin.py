from django.contrib import admin

from link_checker.models import LinkCheck


class LinkCheckAdmin(admin.ModelAdmin):
    list_display = [
        "link",
        "anchor",
        "url",
        "published",
        "created",
    ]


admin.site.register(LinkCheck, LinkCheckAdmin)
