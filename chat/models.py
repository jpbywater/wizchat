from django.db import models

class SavedChat(models.Model):
    id = models.AutoField(primary_key=True)
    ws_group_name = models.CharField(max_length=50)
    timestamp_start = models.DateTimeField(auto_now_add=True)
    timestamp_end = models.DateTimeField(auto_now=True)
    chat_data = models.TextField(blank=True)
    supervisor_role = models.CharField(max_length=50, default="nosupervisor")