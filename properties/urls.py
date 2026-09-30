
from django.urls import path

from .views import (
    property_list,
    property_detail,

    # Management
    property_manage,
    property_create,
    property_edit,
    property_delete,

    # Images
    property_image_add,
    property_image_delete,

    # Videos
    property_video_add,
    property_video_delete,
)


app_name = "properties"


urlpatterns = [

    # =========================================================
    # MANAGEMENT
    # =========================================================

    path(
        "manage/",
        property_manage,
        name="property_manage"
    ),

    path(
        "manage/add/",
        property_create,
        name="property_create"
    ),

    path(
        "manage/<int:pk>/edit/",
        property_edit,
        name="property_edit"
    ),

    path(
        "manage/<int:pk>/delete/",
        property_delete,
        name="property_delete"
    ),


    # =========================================================
    # IMAGES
    # =========================================================

    path(
        "manage/<int:property_id>/images/add/",
        property_image_add,
        name="property_image_add"
    ),

    path(
        "manage/images/<int:image_id>/delete/",
        property_image_delete,
        name="property_image_delete"
    ),


    # =========================================================
    # VIDEOS
    # =========================================================

    path(
        "manage/<int:property_id>/videos/add/",
        property_video_add,
        name="property_video_add"
    ),

    path(
        "manage/videos/<int:video_id>/delete/",
        property_video_delete,
        name="property_video_delete"
    ),


    # =========================================================
    # PUBLIC WEBSITE
    # =========================================================

    path(
        "",
        property_list,
        name="property_list"
    ),

    path(
        "<slug:slug>/",
        property_detail,
        name="property_detail"
    ),

]

