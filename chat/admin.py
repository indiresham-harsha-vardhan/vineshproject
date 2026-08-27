from django.contrib import admin

from .models import (
    ChatConversation,
    ChatMessage
)


class ChatMessageInline(
    admin.TabularInline
):

    model = ChatMessage

    extra = 0

    readonly_fields = (
        "created_at",
    )


@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "email",
        "is_active",
        "created_at",
        "updated_at",
        "reply_button",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
    )

    inlines = [
        ChatMessageInline
    ]

    def reply_button(self, obj):

        from django.utils.html import format_html

        return format_html(
            '<a href="/chat/admin-chat/{}/" '
            'style="background:#8b5e3c;'
            'color:white;'
            'padding:6px 12px;'
            'border-radius:5px;'
            'text-decoration:none;">'
            'Reply'
            '</a>',
            obj.id
        )

    reply_button.short_description = "Chat"

@admin.register(ChatMessage)
class ChatMessageAdmin(
    admin.ModelAdmin
):

    list_display = (
        "conversation",
        "sender",
        "message",
        "created_at",
        "is_read",
    )

    list_filter = (
        "sender",
        "is_read",
        "created_at",
    )

    search_fields = (
        "message",
    )