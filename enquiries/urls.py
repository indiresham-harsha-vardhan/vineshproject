from django.urls import path
from . import views

urlpatterns = [
    path(
        "save-visitor-email/",
        views.save_visitor_email,
        name="save_visitor_email"
    ),
]