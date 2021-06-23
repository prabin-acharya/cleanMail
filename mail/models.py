from django.contrib.auth.models import AbstractUser
from django.db import models



class Email(models.Model):
	user = models.EmailField(max_length=254, blank=True)
	sender = models.EmailField(max_length=254)
	recipients = models.EmailField(max_length=254)
	subject = models.CharField(max_length=255)
	body = models.TextField(blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	read = models.BooleanField(default=False)

	def serialize(self):
		return{
        	"id": self.id,
        	"user": self.user,
        	"sender": self.sender,
        	"recipients": self.recipients,#[user.email for user in self.recipients.all()],
        	"subject": self.subject,
        	"body": self.body,
        	"timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        	"read": self.read,
    	}

	def __str__(self):
		return f"{self.sender} to {self.recipients}"