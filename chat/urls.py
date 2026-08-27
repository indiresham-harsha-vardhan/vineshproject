from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.chat_page,
        name="chat"
    ),

    path(
        "start/",
        views.start_chat,
        name="start_chat"
    ),

    path(
        "send/",
        views.send_message,
        name="send_message"
    ),

    path(
        "messages/",
        views.get_messages,
        name="get_messages"
    ),
    path(
    "admin-chat/<int:conversation_id>/",
    views.admin_chat,
    name="admin_chat"
),
]