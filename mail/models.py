from django.contrib.auth.models import AbstractUser
from django.db import models



class Email(models.Model):
	user = models.EmailField(max_length=254)
	gmail_id = models.CharField(max_length=32)
	sender = models.EmailField(max_length=254)
	sender_email = models.EmailField(max_length=254)
	recipients = models.EmailField(max_length=254)
	recipients_email = models.EmailField(max_length=254)
	subject = models.CharField(max_length=255)
	body = models.TextField()
	timestamp = models.DateTimeField()
	read = models.BooleanField(default=False)

	def serialize(self):
		return{
        	"id": self.id,
        	"gmail_id": self.gmail_id,
        	"user": self.user,
        	"sender": self.sender,
        	"sender_email": self.sender_email,
        	"recipients": self.recipients,
        	"recipients_email": self.recipients_email,
        	"subject": self.subject,
        	"body": self.body,
        	"timestamp": self.timestamp.astimezone().strftime("%b %d %Y, %I:%M %p"),
        	"read": self.read,
    	}

	def __str__(self):
		return f"{self.sender} to {self.recipients}"