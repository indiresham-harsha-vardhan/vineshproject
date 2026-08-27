from django.urls import path

from . import views


urlpatterns = [

    path(
        "properties/",
        views.property_list,
        name="property_list"
    ),

    path(
        "properties/<slug:slug>/",
        views.property_detail,
        name="property_detail"
    ),
     path(
        "save-visitor-email/",
        views.save_visitor_email,
        name="save_visitor_email"
    ),
    

]