
"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from properties.views import home
from enquiries.views import contact
from about.views import about_us

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # =========================================================
    # DJANGO ADMIN
    # =========================================================

    path(
        "admin/",
        admin.site.urls
    ),

    path(
    "accounts/login/",
    auth_views.LoginView.as_view(
        template_name="registration/login.html"
    ),
    name="login"
),
    # =========================================================
    # HOME
    # =========================================================

    path(
        "",
        home,
        name="home"
    ),


    # =========================================================
    # PROPERTIES
    # =========================================================

    path(
        "properties/",
        include("properties.urls")
    ),


    # =========================================================
    # CONTACT
    # =========================================================

    path(
        "contact/",
        contact,
        name="contact"
    ),


    # =========================================================
    # ABOUT
    # =========================================================

    path(
        "about/",
        about_us,
        name="about"
    ),


    # =========================================================
    # CHAT
    # =========================================================

    path(
        "chat/",
        include("chat.urls")
    ),


    # =========================================================
    # ENQUIRIES
    # =========================================================

    path(
        "enquiries/",
        include("enquiries.urls")
    ),

]


# =============================================================
# MEDIA FILES
# =============================================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

