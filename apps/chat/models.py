from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name="chat_room")

    def __str__(self) -> str:
        return f"{self.name}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Check if the sender is a member of the chat room
        if self.sender not in self.chat_room.users.all():
            raise ValidationError("The sender is not a member of the chat room.")
        super().clean()

    def __str__(self) -> str:
        return f"{self.sender.username} - {self.content[0:50]}"
