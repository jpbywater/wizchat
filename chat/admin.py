from django.contrib import admin

from .models import SavedChat

class SavedChatAdmin(admin.ModelAdmin):
    list_display = ('ws_group_name', 'supervisor_role', 'timestamp_start', 'timestamp_end', 'chat_data')

admin.site.register(SavedChat, SavedChatAdmin)
