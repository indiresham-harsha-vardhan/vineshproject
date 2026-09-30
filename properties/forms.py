
from django import forms

from .models import (
    Property,
    PropertyImage,
    PropertyVideo,
)


# ============================================================
# PROPERTY FORM
# ============================================================

class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property

        fields = [
            "title",
            "property_type",
            "description",

            "price",
            "price_type",

            "location",
            "city",
            "state",
            "pincode",
            "address",

            "latitude",
            "longitude",

            "area_sqft",
            "plot_area",
            "built_up_area",

            "bedrooms",
            "bathrooms",
            "floors",
            "parking",

            "facing",
            "furnishing",

            "amenities",

            "status",
            "featured",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter property title"
                }
            ),

            "property_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Describe the property..."
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter price",
                    "step": "0.01"
                }
            ),

            "price_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Locality / Area"
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "City"
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "State"
                }
            ),

            "pincode": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Pincode"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Complete address"
                }
            ),

            "latitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Latitude",
                    "step": "0.0000001"
                }
            ),

            "longitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Longitude",
                    "step": "0.0000001"
                }
            ),

            "area_sqft": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Total area",
                    "step": "0.01"
                }
            ),

            "plot_area": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Plot area",
                    "step": "0.01"
                }
            ),

            "built_up_area": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Built-up area",
                    "step": "0.01"
                }
            ),

            "bedrooms": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Bedrooms",
                    "min": "0"
                }
            ),

            "bathrooms": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Bathrooms",
                    "min": "0"
                }
            ),

            "floors": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Number of floors",
                    "min": "0"
                }
            ),

            "parking": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Parking spaces",
                    "min": "0"
                }
            ),

            "facing": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "furnishing": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "amenities": forms.SelectMultiple(
                attrs={
                    "class": "form-select",
                    "size": "6"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "featured": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }


# ============================================================
# IMAGE FORM
# ============================================================

class PropertyImageForm(forms.ModelForm):

    class Meta:
        model = PropertyImage

        fields = [
            "image",
            "title",
            "is_primary",
        ]

        widgets = {

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*"
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Image title"
                }
            ),

            "is_primary": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }


# ============================================================
# VIDEO FORM
# ============================================================

class PropertyVideoForm(forms.ModelForm):

    class Meta:
        model = PropertyVideo

        fields = [
            "video",
            "video_url",
            "title",
        ]

        widgets = {

            "video": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "video/*"
                }
            ),

            "video_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://youtube.com/..."
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Video title"
                }
            ),
        }

