from django.contrib.auth.models import AbstractUser
from django.db import models



class Email(models.Model):
	user = models.EmailField(max_length=254, blank=True)
	gmail_id = models.CharField(max_length=32, blank=True)
	sender = models.EmailField(max_length=254)
	recipients = models.EmailField(max_length=254)
	recipients_email = models.EmailField(max_length=254)
	subject = models.CharField(max_length=255, blank=True)
	body = models.TextField(blank=True)
	timestamp = models.DateTimeField(blank=True)
	read = models.BooleanField(default=False)

	def serialize(self):
		return{
        	"id": self.id,
        	"gmail_id": self.gmail_id,
        	"user": self.user,
        	"sender": self.sender,
        	"recipients": self.recipients,#[user.ema
        	"subject": self.subject,
        	"body": self.body,
        	"timestamp": self.timestamp.astimezone().strftime("%b %d %Y, %I:%M %p"),
        	"read": self.read,
    	}

	def __str__(self):
		return f"{self.sender} to {self.recipients}"