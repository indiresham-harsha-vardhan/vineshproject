from django.shortcuts import render, get_object_or_404,redirect
from .models import Property,PropertyType
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import *
from .forms import PropertyForm


def home(request):

    featured_properties = Property.objects.filter(
        featured=True,
        status="available"
    ).select_related(
        "property_type"
    ).prefetch_related(
        "images"
    )[:6]


    latest_properties = Property.objects.filter(
        status="available"
    ).select_related(
        "property_type"
    ).prefetch_related(
        "images"
    ).order_by(
        "-created_at"
    )[:6]


    property_types = PropertyType.objects.all()


    context = {

        "featured_properties":
            featured_properties,

        "latest_properties":
            latest_properties,

        "property_types":
            property_types,

    }


    return render(
        request,
        "home.html",
        context
    )




def property_list(request):

    properties = Property.objects.filter(
        status="available"
    ).select_related(
        "property_type"
    ).prefetch_related(
        "images",
        "amenities"
    ).order_by(
        "-created_at"
    )


    # Search

    search = request.GET.get(
        "search",
        ""
    ).strip()


    if search:

        properties = properties.filter(

            title__icontains=search

        ) | properties.filter(

            location__icontains=search

        ) | properties.filter(

            city__icontains=search

        )


    # Property type

    property_type = request.GET.get(
        "type",
        ""
    ).strip()


    if property_type:

        properties = properties.filter(
            property_type__slug=property_type
        )


    # Location

    location = request.GET.get(
        "location",
        ""
    ).strip()


    if location:

        properties = properties.filter(
            city__icontains=location
        )


    # Price

    min_price = request.GET.get(
        "min_price",
        ""
    ).strip()


    max_price = request.GET.get(
        "max_price",
        ""
    ).strip()


    if min_price:

        try:

            properties = properties.filter(
                price__gte=float(min_price)
            )

        except ValueError:

            pass


    if max_price:

        try:

            properties = properties.filter(
                price__lte=float(max_price)
            )

        except ValueError:

            pass


    property_types = PropertyType.objects.all()


    context = {

        "properties":
            properties,

        "property_types":
            property_types,

        "search":
            search,

        "selected_type":
            property_type,

        "location":
            location,

        "min_price":
            min_price,

        "max_price":
            max_price,

    }


    return render(
        request,
        "properties.html",
        context
    )

def property_detail(request, slug):

    property_obj = get_object_or_404(
        Property.objects.select_related(
            "property_type"
        ).prefetch_related(
            "images",
            "videos",
            "amenities"
        ),
        slug=slug
    )

    context = {
        "property": property_obj,
    }

    return render(
        request,
        "properties/property_detail.html",
        context
    )




@require_POST
@csrf_protect
def save_visitor_email(request):

    email = request.POST.get("email", "").strip().lower()

    if not email:
        return JsonResponse({
            "success": False,
            "message": "Email is required."
        }, status=400)

    # Basic Django email validation
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({
            "success": False,
            "message": "Please enter a valid email address."
        }, status=400)

    # Don't create duplicate emails
    visitor, created = VisitorEmail.objects.get_or_create(
        email=email
    )

    return JsonResponse({
        "success": True,
        "message": "Email saved successfully."
    })


def add_property(request):

    if request.method == "POST":

        form = PropertyForm(request.POST)

        if form.is_valid():

            # -----------------------------
            # SAVE PROPERTY
            # -----------------------------

            property_obj = form.save()


            # -----------------------------
            # SAVE PROPERTY IMAGES
            # -----------------------------

            images = request.FILES.getlist("images")

            image_titles = request.POST.getlist("image_titles")

            primary_image = request.POST.get("primary_image")


            for index, image in enumerate(images):

                title = ""

                if index < len(image_titles):
                    title = image_titles[index]


                is_primary = (
                    str(index) == str(primary_image)
                )


                PropertyImage.objects.create(
                    property=property_obj,
                    image=image,
                    title=title,
                    is_primary=is_primary
                )


            # -----------------------------
            # SAVE PROPERTY VIDEOS
            # -----------------------------

            videos = request.FILES.getlist("videos")

            video_titles = request.POST.getlist("video_titles")


            for index, video in enumerate(videos):

                title = ""

                if index < len(video_titles):
                    title = video_titles[index]


                PropertyVideo.objects.create(
                    property=property_obj,
                    video=video,
                    title=title
                )


            # -----------------------------
            # SAVE VIDEO URL
            # -----------------------------

            video_url = request.POST.get("video_url")

            video_url_title = request.POST.get("video_url_title")


            if video_url:

                PropertyVideo.objects.create(
                    property=property_obj,
                    video_url=video_url,
                    title=video_url_title or ""
                )


            messages.success(
                request,
                f"Property {property_obj.property_id} created successfully!"
            )


            return redirect("properties:add-property")


    else:

        form = PropertyForm()


    return render(
        request,
        "properties/add_property.html",
        {
            "form": form
        }
    )