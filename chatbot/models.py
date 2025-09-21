from django.db import models
from django.contrib .auth.models import User
from django.http import response
# Create your models here.

class Chat(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # This function returns a string representation of the Chat object,
    # showing the username of the user and their message.
    def __str__(self):
        return f'{self.user.username}: {self.message}'
