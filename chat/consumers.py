import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import SavedChat
from chat.nlp import to_user
import ast


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = self.scope["session"]["ws_group_name"] + str(self.scope["session"]["chat_pk"])
        print("GN:", self.group_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        # Send new msg about conversation ending
        try:
            if self.scope["session"]["supervisor_role"]:
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        'type': 'chat_message',  # name of function to call
                        'from': 'System',
                        'text': 'Student left the chat<br><a href="/chat/start">[Start conversation over]</a>',
                        'image': ''
                    }
                )
        except:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'chat_message',  # name of function to call
                    'from': 'System',
                    'text': 'Teacher left the chat<br><a href="/chat/ozstart">[Restart supervision]</a>',
                    'image': ''
                }
            )

    # Receive message from WebSocket
    def receive(self, text_data):
        # Unpack message
        msg_json = json.loads(text_data)
        msg_from = msg_json['from']
        msg_text = msg_json['text']
        msg_image = msg_json['image']

        # Get chat_pk and supervisor_role
        chat_pk = self.scope["session"]["chat_pk"]
        supervisor_role = SavedChat.objects.get(pk=chat_pk).supervisor_role
        trial_id = SavedChat.objects.get(pk=chat_pk).trial_id

        # Append new msg to DB record
        chat_data = ast.literal_eval(SavedChat.objects.get(pk=chat_pk).chat_data)
        chat_data.append({'from': msg_from, 'text': msg_text, 'image': msg_image})
        SavedChat.objects.filter(pk=chat_pk).update(chat_data=str(chat_data))
        SavedChat.objects.get(pk=chat_pk).save()  #updates DB record timestamp

        # Send new msg to group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat_message',  # name of function to call
                'from': msg_from,
                'text': msg_text,
                'image': msg_image
            }
        )

        # If new message is from participant, respond again (with nlp or supervisor)
        if msg_from == "Teacher":
            if supervisor_role in ["nosupervisor", "observer", "verify", "backup"]:
                # Send new msg and prior_chat_data to NLP
                nlp_from, nlp_text, nlp_image = to_user(msg_text, msg_image, chat_data, trial_id)
                # Append nlp msg to DB record
                chat_data.append({'from': nlp_from, 'text': nlp_text, 'image': nlp_image})
                SavedChat.objects.filter(pk=chat_pk).update(chat_data=str(chat_data))
                SavedChat.objects.get(pk=chat_pk).save()  # updates DB record timestamp

            if supervisor_role == "solo":
                # Send blank msg as helpee to activate ozchat interface and don't save to DB
                nlp_from = "Helpee"
                nlp_text = ''
                nlp_image = msg_image

            if supervisor_role == "nosupervisor" or supervisor_role == "observer":
                # Override nlp_from to always be "Student" (even if AI needs help)
                nlp_from = "Student"

            if supervisor_role == "verify":
                # Override nlp_from to always be "Helpee" (even if AI doesn't need help)
                nlp_from = "Helpee"

            # Send nlp msg to group
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'chat_message', # name of function to call
                    'from': nlp_from,
                    'text': nlp_text,
                    'image': nlp_image
                }
            )

    # Send message from room group to group members
    def chat_message(self, event):
        self.send(json.dumps({
            'from': event['from'],
            'text': event['text'],
            'image': event['image']
        }))
