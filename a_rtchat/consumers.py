from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import *
import json
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
'''ChatroomConsumer được sử dụng để xử lý các sự kiện WebSocket.
 Consumer trong Django Channels là một thành phần chịu trách nhiệm 
 quản lý các kết nối và tương tác giữa máy chủ và client qua giao thức WebSocket.'''
'''Lớp ChatroomConsumer thường được sử dụng trong các ứng dụng chat trực tuyến, nơi cần xử lý các sự kiện như:

Kết nối WebSocket: Khi người dùng tham gia phòng chat.
Ngắt kết nối WebSocket: Khi người dùng rời khỏi phòng chat.
Nhận tin nhắn: Khi người dùng gửi tin nhắn qua WebSocket, tin nhắn này sẽ được nhận,
 xử lý và gửi lại tới tất cả người dùng khác trong phòng chat.'''
class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user=self.scope['user']
        self.chatroom_name=self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom=get_object_or_404(ChatGroup, group_name=self.chatroom_name)

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,self.channel_name
        )

        # add and update online users
        if self.user  not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()

        self.accept()
    #hàm ngắt kết nối kênh của client khi client này không còn hoạt động.
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,self.channel_name
        )
        
        # remove and update online users
        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()


    def receive(self, text_data):
        text_data_json=json.loads(text_data)
        body=text_data_json['body']

        message=GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom ,
        )
        event={
            'type': 'message_handler',
            'message_id':message.id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def message_handler(self, event):
        message_id=event['message_id']
        message=GroupMessage.objects.get(id=message_id)
        context={
            'message': message,
            'user': self.user,
        }
        html=render_to_string("partials/chat_message_p.html",context)
        self.send(text_data=html)

    def update_online_count(self):
        online_count=self.chatroom.users_online.count()-1
        event={
            'type': 'online_count_handler',
            'online_count': online_count,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def online_count_handler(self, event):
        online_count=event['online_count']
        context={
            'online_count': online_count,
            'chat_group': self.chatroom,
        }
        html=render_to_string("partials/online_count.html",context)
        self.send(text_data=html)

