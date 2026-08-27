from django.contrib import admin

from .models import Enquiry,VisitorEmail


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "email",
        "enquiry_type",
        "property",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "enquiry_type",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "message",
        "property__title",
        "property__property_id",
    )

    list_editable = (
        "status",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(VisitorEmail)
class VisitorEmailAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "created_at",
    )

    search_fields = (
        "email",
    )

    ordering = (
        "-created_at",
    )