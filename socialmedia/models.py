from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True, null=False)
    profile_img = models.ImageField(upload_to="social-a-media/profile-images/", default="social-a-media/blank-profile-picture.png")
    location = models.CharField(max_length=120, blank=True, null=False)
    
    def __str__(self):
        return self.user.username
    
    
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient_username = models.CharField(max_length=120, blank=False, null=False)
    recipient_profile_img = models.CharField(max_length=1200, blank=False, null=False)
    conversation_id = models.IntegerField()
    
    def __str__(self):
        return self.recipient
    
    
class Message(models.Model):
    sender = models.CharField(max_length=120, blank=False, null=False)
    recipient = models.CharField(max_length=120, blank=False, null=False)
    message = models.TextField(max_length=100000, blank=False, null=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    conversation_id = models.IntegerField()
    
    def __str__(self):
        return self.message


    