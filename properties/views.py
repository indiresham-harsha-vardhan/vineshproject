from django.shortcuts import render, get_object_or_404,redirect
from .models import Property,PropertyType
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import *
from .forms import PropertyForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from .models import (
    Property,
    PropertyImage,
    PropertyVideo,
)

from .forms import (
    PropertyForm,
    PropertyImageForm,
    PropertyVideoForm,
)



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


# ============================================================
# PROPERTY MANAGEMENT
# ============================================================


@login_required
def property_manage(request):

    properties = Property.objects.select_related(
        "property_type"
    ).prefetch_related(
        "images"
    ).all()

    context = {
        "properties": properties,
    }

    return render(
        request,
        "properties/property_manage.html",
        context
    )


# ============================================================
# ADD PROPERTY
# ============================================================


@login_required
def property_create(request):

    if request.method == "POST":

        form = PropertyForm(
            request.POST
        )

        if form.is_valid():

            property_obj = form.save()

            messages.success(
                request,
                f"Property {property_obj.property_id} created successfully."
            )

            return redirect(
                "properties:property_edit",
                pk=property_obj.pk
            )

    else:

        form = PropertyForm()


    context = {
        "form": form,
        "property_obj": None,
        "images": [],
        "videos": [],
        "page_title": "Add Property",
    }

    return render(
        request,
        "properties/property_form.html",
        context
    )


# ============================================================
# EDIT PROPERTY
# ============================================================


@login_required
def property_edit(request, pk):

    property_obj = get_object_or_404(
        Property,
        pk=pk
    )

    if request.method == "POST":

        form = PropertyForm(
            request.POST,
            instance=property_obj
        )

        if form.is_valid():

            property_obj = form.save()

            messages.success(
                request,
                "Property updated successfully."
            )

            return redirect(
                "properties:property_edit",
                pk=property_obj.pk
            )

    else:

        form = PropertyForm(
            instance=property_obj
        )


    images = property_obj.images.all()
    videos = property_obj.videos.all()


    context = {
        "form": form,
        "property_obj": property_obj,
        "images": images,
        "videos": videos,
        "page_title": "Edit Property",
    }


    return render(
        request,
        "properties/property_form.html",
        context
    )


# ============================================================
# DELETE PROPERTY
# ============================================================


@login_required
def property_delete(request, pk):

    property_obj = get_object_or_404(
        Property,
        pk=pk
    )

    if request.method == "POST":

        property_id = property_obj.property_id

        property_obj.delete()

        messages.success(
            request,
            f"Property {property_id} deleted successfully."
        )

        return redirect(
            "properties:property_manage"
        )


    return render(
        request,
        "properties/property_confirm_delete.html",
        {
            "property_obj": property_obj
        }
    )


# ============================================================
# ADD IMAGE
# ============================================================


@login_required
def property_image_add(
    request,
    property_id
):

    property_obj = get_object_or_404(
        Property,
        pk=property_id
    )


    if request.method == "POST":

        form = PropertyImageForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            image = form.save(
                commit=False
            )

            image.property = property_obj

            # If this image is primary,
            # remove primary from existing images.
            if image.is_primary:

                PropertyImage.objects.filter(
                    property=property_obj
                ).update(
                    is_primary=False
                )

            image.save()

            messages.success(
                request,
                "Image uploaded successfully."
            )

            return redirect(
                "properties:property_edit",
                pk=property_obj.pk
            )

    else:

        form = PropertyImageForm()


    return render(
        request,
        "properties/property_image_form.html",
        {
            "form": form,
            "property_obj": property_obj,
        }
    )


# ============================================================
# DELETE IMAGE
# ============================================================


@login_required
def property_image_delete(
    request,
    image_id
):

    image = get_object_or_404(
        PropertyImage,
        pk=image_id
    )

    property_obj = image.property


    if request.method == "POST":

        image.delete()

        messages.success(
            request,
            "Image deleted successfully."
        )

        return redirect(
            "properties:property_edit",
            pk=property_obj.pk
        )


    return render(
        request,
        "properties/property_confirm_image_delete.html",
        {
            "image": image,
            "property_obj": property_obj,
        }
    )


# ============================================================
# ADD VIDEO
# ============================================================


@login_required
def property_video_add(
    request,
    property_id
):

    property_obj = get_object_or_404(
        Property,
        pk=property_id
    )


    if request.method == "POST":

        form = PropertyVideoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            video = form.save(
                commit=False
            )

            video.property = property_obj

            video.save()

            messages.success(
                request,
                "Video added successfully."
            )

            return redirect(
                "properties:property_edit",
                pk=property_obj.pk
            )

    else:

        form = PropertyVideoForm()


    return render(
        request,
        "properties/property_video_form.html",
        {
            "form": form,
            "property_obj": property_obj,
        }
    )


# ============================================================
# DELETE VIDEO
# ============================================================


@login_required
def property_video_delete(
    request,
    video_id
):

    video = get_object_or_404(
        PropertyVideo,
        pk=video_id
    )

    property_obj = video.property


    if request.method == "POST":

        video.delete()

        messages.success(
            request,
            "Video deleted successfully."
        )

        return redirect(
            "properties:property_edit",
            pk=property_obj.pk
        )


    return render(
        request,
        "properties/property_confirm_video_delete.html",
        {
            "video": video,
            "property_obj": property_obj,
        }
    )

