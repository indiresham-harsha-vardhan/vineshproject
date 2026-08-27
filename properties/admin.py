
from django.contrib import admin
from .models import (
    PropertyType,
    Amenity,
    Property,
    PropertyImage,
    PropertyVideo,
    Venture,
    VenturePlot,
  
)


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "icon",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class PropertyVideoInline(admin.TabularInline):
    model = PropertyVideo
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        "property_id",
        "title",
        "property_type",
        "city",
        "price",
        "status",
        "featured",
        "created_at",
    )

    list_filter = (
        "property_type",
        "status",
        "featured",
        "city",
        "furnishing",
        "facing",
    )

    search_fields = (
        "property_id",
        "title",
        "location",
        "city",
        "state",
        "description",
    )

    list_editable = (
        "status",
        "featured",
    )

    readonly_fields = (
        "property_id",
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    filter_horizontal = (
        "amenities",
    )

    inlines = [
        PropertyImageInline,
        PropertyVideoInline,
    ]

    fieldsets = (

        (
            "Basic Information",
            {
                "fields": (
                    "property_id",
                    "title",
                    "slug",
                    "property_type",
                    "description",
                )
            }
        ),

        (
            "Price",
            {
                "fields": (
                    "price",
                    "price_type",
                )
            }
        ),

        (
            "Location",
            {
                "fields": (
                    "location",
                    "city",
                    "state",
                    "pincode",
                    "address",
                    "latitude",
                    "longitude",
                )
            }
        ),

        (
            "Area",
            {
                "fields": (
                    "area_sqft",
                    "plot_area",
                    "built_up_area",
                )
            }
        ),

        (
            "Property Details",
            {
                "fields": (
                    "bedrooms",
                    "bathrooms",
                    "floors",
                    "parking",
                    "facing",
                    "furnishing",
                )
            }
        ),

        (
            "Amenities",
            {
                "fields": (
                    "amenities",
                )
            }
        ),

        (
            "Status",
            {
                "fields": (
                    "status",
                    "featured",
                )
            }
        ),

        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),
    )


@admin.register(Venture)
class VentureAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "city",
        "total_area",
        "total_plots",
        "available_plots",
        "sold_plots",
    )

    search_fields = (
        "name",
        "location",
        "city",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(VenturePlot)
class VenturePlotAdmin(admin.ModelAdmin):

    list_display = (
        "venture",
        "plot_number",
        "area",
        "price",
        "status",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "plot_number",
        "venture__name",
    )

