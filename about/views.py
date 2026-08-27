from django.shortcuts import render

from .models import AboutUs


def about_us(request):

    about = AboutUs.objects.filter(
        is_active=True
    ).first()

    return render(
        request,
        "about.html",
        {
            "about": about
        }
    )