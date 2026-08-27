from django.contrib import messages
from django.shortcuts import redirect, render

from properties.models import Property

from .models import Enquiry


def contact(request):

    property_id = request.GET.get("property")

    selected_property = None

    if property_id:

        selected_property = Property.objects.filter(
            property_id=property_id
        ).first()

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        enquiry_type = request.POST.get(
            "enquiry_type",
            "general"
        )

        message = request.POST.get(
            "message"
        )

        property_id = request.POST.get(
            "property_id"
        )

        selected_property = None

        if property_id:

            selected_property = Property.objects.filter(
                property_id=property_id
            ).first()

        Enquiry.objects.create(

            name=name,

            email=email,

            phone=phone,

            enquiry_type=enquiry_type,

            property=selected_property,

            message=message,
        )

        messages.success(
            request,
            "Thank you! Our team will contact you shortly."
        )

        return redirect(
            "contact"
        )

    context = {
        "selected_property": selected_property,
    }

    return render(
        request,
        "contact.html",
        context
    )