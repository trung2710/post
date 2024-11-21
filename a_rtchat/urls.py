from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_view, name='chathome'),
    path('chat/<username>/', views.get_or_create_chatroom, name='start-chat'),
    path('chat/room/<chatroom_name>/',views.chat_view, name='chatroom' ),
    path('new/groupchat', views.create_groupchat, name="new-groupchat"),
    path('chat/edit/<chatroom_name>/', views.chatroom_edit_view, name='edit-chatroom'),
    path('chat/delete/<chatroom_name>/', views.chatroom_delete_view, name='chatroom-delete'),
    path('chat/leave/<chatroom_name>', views.chatroom_leave_view, name='chatroom-leave'),
    path('chat/add/<chatroom_name>', views.chatroom_add_view, name='chatroom-add'),
    #phan quyen admin chap nhan user vao nhom.
    path('chat/request_join/<str:chatroom_name>/', views.chat_view, name='request_join_chatroom'),
    path('chat/review_requests/<str:chatroom_name>/', views.review_join_requests, name='review_join_requests'),
    path('chat/handle_request/<request_id>/<action>/', views.handle_join_request, name='handle_join_request'),
    #gui file trong doan chat
    path('chat/fileupload/<chatroom_name>/', views.chat_file_upload, name="chat-file-upload"),
]
