from django.contrib import admin

from .models import MailingEmailAddress


@admin.register(MailingEmailAddress)
class MailingEmailAddressModelAdmin(admin.ModelAdmin):
    """Admin class for the managing MailingEmailAddress instances."""

    list_filter = ["created"]
    search_fields = ["email"]
    readonly_fields = ["id", "created"]
    search_help_text = "Searching by email address."
    list_display = fields = ["id", "email", "created"]
