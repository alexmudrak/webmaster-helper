from django.contrib import admin

from api.webmaster.models import (
    Contact,
    ContactHistory,
    Payment,
    PaymentHistory,
    PublishPage,
    Webmaster,
    Website,
)


class PublishPageAdmin(admin.ModelAdmin):
    list_display = (
        "website",
        "get_owner",
        "get_project_name",
        # "get_webmaster",
        "url",
        "check_status",
    )

    @admin.display(description="Owner")
    def get_owner(self, obj):
        return obj.project.owner.username

    @admin.display(description="Project")
    def get_project_name(self, obj):
        return obj.project.name

    @admin.display(description="Webmaster")
    def get_webmaster(self, obj):
        webmasters = obj.website.webmaster.all()
        if webmasters:
            return ", ".join(webmaster.name for webmaster in webmasters)
        else:
            return "-"


admin.site.register(Webmaster)
admin.site.register(Contact)
admin.site.register(ContactHistory)
admin.site.register(Payment)
admin.site.register(PaymentHistory)
admin.site.register(PublishPage, PublishPageAdmin)
admin.site.register(Website)
