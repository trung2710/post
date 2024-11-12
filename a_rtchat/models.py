from django.db import models
from django.contrib.auth.models import User
import shortuuid
import uuid
class ChatGroup(models.Model):
    group_name=models.CharField(max_length=128, unique=True,default=shortuuid.uuid)
    admin=models.ForeignKey(User,related_name='groupadmin', null=True, blank=True, on_delete=models.SET_NULL )
    groupchat_name=models.CharField(max_length=128, null=True, blank=True)
    users_online=models.ManyToManyField(User, related_name='online_in_groups', blank=True)
    members=models.ManyToManyField(User, related_name='chat_groups', blank=True)
    is_private=models.BooleanField(default=False)

    def __str__(self):
        return self.group_name
    

class GroupMessage(models.Model):
    group=models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    body=models.CharField(max_length=300)
    created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.author.username}:{self.body}'
    
    class Meta:
        ordering = ['-created']

class JoinRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="join_requests")
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name="join_requests")
    status = models.CharField(max_length=10, choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")], default="pending")
    created = models.DateTimeField(auto_now_add=True)
    request_name=models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    def __str__(self):
        return f"{self.user.username} - {self.chat_group.group_name} ({self.status})"
    
    class Meta:
        ordering=['-created']