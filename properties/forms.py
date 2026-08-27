from django import forms
from .models import Property


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

            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter property title"
            }),

            "property_type": forms.Select(attrs={
                "class": "form-control"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Enter property description"
            }),

            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter property price",
                "step": "0.01"
            }),

            "price_type": forms.Select(attrs={
                "class": "form-control"
            }),

            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Area / Location"
            }),

            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "City"
            }),

            "state": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "State"
            }),

            "pincode": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Pincode"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Complete address"
            }),

            "latitude": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "any",
                "placeholder": "Latitude"
            }),

            "longitude": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "any",
                "placeholder": "Longitude"
            }),

            "area_sqft": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),

            "plot_area": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),

            "built_up_area": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),

            "bedrooms": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0"
            }),

            "bathrooms": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0"
            }),

            "floors": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0"
            }),

            "parking": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0"
            }),

            "facing": forms.Select(attrs={
                "class": "form-control"
            }),

            "furnishing": forms.Select(attrs={
                "class": "form-control"
            }),

            "status": forms.Select(attrs={
                "class": "form-control"
            }),

            "featured": forms.CheckboxInput(attrs={
                "class": "featured-checkbox"
            }),
        }