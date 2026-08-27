from django.contrib import admin

from .models import AboutUs


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):

    list_display = (
        "company_name",
        "heading",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "company_name",
        "heading",
        "description",
    )