from django.contrib import admin

from mail.models import Mail, MailSettings


class MailAdmin(admin.ModelAdmin):
    list_display = [
        "mail_settings",
        "mail_box",
        "author_name",
        "author_mail",
        "subject",
        "receive_date",
        "mail_id",
        "replay_to",
    ]


admin.site.register(Mail, MailAdmin)
admin.site.register(MailSettings)
