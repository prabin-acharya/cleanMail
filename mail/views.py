from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

import json
from .models import Email
from . import gmailapi

user = gmailapi.service.users().getProfile(userId='me').execute()['emailAddress']

# Create your views here.

def index(request):
    return render(request, "mail/inbox.html", {"user":user})

@csrf_exempt
def mailbox(request, mailbox):
    Email.objects.all().delete()
    gmailapi.Prabin()
    gmailapi.sent_gmails()
    if mailbox == "inbox":
        emails = Email.objects.filter(recipients=user)
    elif mailbox == "sent":
        emails = Email.objects.filter(sender=user)
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)
    #emails = Email.objects.all()
    emails = emails.order_by("timestamp").all()
    return JsonResponse([email.serialize() for email in emails], safe=False)

@csrf_exempt
def email(request, email_id):

    # Query for requested email
    try:
        email = Email.objects.get(pk=email_id)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(email.serialize())

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
def compose(request):

    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)

    # Get contents of email
    sender = user
    recipients = data.get("recipients", "")
    subject = data.get("subject", "")
    body = data.get("body", "")
    email = Email(
        sender=sender,
        recipients=recipients,
        subject=subject,
        body=body)
    email.save()
    gmailapi.send_gmail(recipients, subject, body)

    return JsonResponse({"message": "Email sent successfully."}, status=201)
