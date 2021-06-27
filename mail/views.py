from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
#from django.views.decorators.csrf import csrf_exempt

import json
from .models import Email
from . import gmailapi
import datetime

user = gmailapi.service.users().getProfile(userId='me').execute()['emailAddress']

def index(request):
    Email.objects.all().delete()
    gmailapi.get_inbox_gmails()
    gmailapi.get_sent_gmails()
    return render(request, "mail/inbox.html", {"user":user})

def mailbox(request, mailbox):
    if mailbox == "inbox":
        emails = Email.objects.filter(recipients_email=user)
    elif mailbox == "sent":
        emails = Email.objects.filter(sender_email=user)
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)
    emails = emails.order_by("-timestamp").all()
    return JsonResponse([email.serialize() for email in emails], safe=False)

def email(request, email_id):
    # Query for requested email
    try:
        email = Email.objects.get(pk=email_id)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(email.serialize())

    # Update whether email is read
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("read") is not None:
            email.read = data["read"]
            gmail_id = email.gmail_id
            gmailapi.service.users().messages().modify(userId='me', id=gmail_id, body={'removeLabelIds': ['UNREAD']}).execute()
        email.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

def compose(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    # Get contents of email
    sender = data.get("sender", "")
    recipients = data.get("recipients", "")
    subject = data.get("subject", "")
    body = data.get("body", "")
    email = Email(
        sender=sender,
        sender_email=sender,
        recipients=recipients,
        recipients_email=recipients,
        subject=subject,
        timestamp=datetime.datetime.now().astimezone(),
        body=body)
    email.save()
    gmailapi.send_gmail(recipients, subject, body)

    return JsonResponse({"message": "Email sent successfully."}, status=201)
