from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import (
    ChatConversation,
    ChatMessage
)


def chat_page(request):

    return render(
        request,
        "chat.html"
    )


def start_chat(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "message": "Invalid request"
            },
            status=400
        )


    name = request.POST.get(
        "name",
        ""
    ).strip()

    phone = request.POST.get(
        "phone",
        ""
    ).strip()

    email = request.POST.get(
        "email",
        ""
    ).strip()


    if not name or not phone:

        return JsonResponse(
            {
                "success": False,
                "message":
                    "Name and phone are required."
            },
            status=400
        )


    conversation = ChatConversation.objects.create(

        name=name,

        phone=phone,

        email=email or None

    )


    return JsonResponse(
        {
            "success": True,

            "conversation_id":
                conversation.id
        }
    )


def send_message(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False
            },
            status=400
        )


    conversation_id = request.POST.get(
        "conversation_id"
    )

    message = request.POST.get(
        "message",
        ""
    ).strip()


    if not conversation_id or not message:

        return JsonResponse(
            {
                "success": False,

                "message":
                    "Message cannot be empty."
            },
            status=400
        )


    try:

        conversation = (
            ChatConversation.objects.get(
                id=conversation_id,
                is_active=True
            )
        )

    except ChatConversation.DoesNotExist:

        return JsonResponse(
            {
                "success": False,

                "message":
                    "Conversation not found."
            },
            status=404
        )


    ChatMessage.objects.create(

        conversation=conversation,

        message=message,

        sender="visitor"

    )


    return JsonResponse(
        {
            "success": True
        }
    )


def get_messages(request):

    conversation_id = request.GET.get(
        "conversation_id"
    )


    if not conversation_id:

        return JsonResponse(
            {
                "success": False
            },
            status=400
        )


    messages = ChatMessage.objects.filter(

        conversation_id=conversation_id

    ).order_by(
        "created_at"
    )


    data = []


    for item in messages:

        data.append(
            {
                "id": item.id,

                "message": item.message,

                "sender": item.sender,

                "created_at":
                    item.created_at.strftime(
                        "%H:%M"
                    )
            }
        )


    return JsonResponse(
        {
            "success": True,

            "messages": data
        }
    )


@staff_member_required
def admin_chat(request, conversation_id):

    conversation = ChatConversation.objects.get(
        id=conversation_id
    )

    if request.method == "POST":

        message = request.POST.get(
            "message",
            ""
        ).strip()

        if message:

            ChatMessage.objects.create(

                conversation=conversation,

                message=message,

                sender="admin"

            )

            conversation.save()

    messages = ChatMessage.objects.filter(
        conversation=conversation
    ).order_by(
        "created_at"
    )

    return render(
        request,
        "chat/admin_chat.html",
        {
            "conversation": conversation,
            "messages": messages,
        }
    )