# mail-Gmail

mail-Gmail loads user's Gmail inbox and presents it in a web view.

Displays all of user's unread emails, sent emails and allows them to send and reply to emails using Gmail RESTful API.

I had the idea about this project when working on my another project [mail](https://github.com/prabin-acharya/mail) where users can Sign in and send emails among users.



## Setup
Before working on this repository, you have to set up a project on [Google Console](https://console.cloud.google.com/). I have written an article about it for Gmail API. You can refer to that [here](https://dev.to/pra6in).

After that, 

Clone this repository.
```bash
git clone https://github.com/prabin-acharya/mail-Gmail
cd mail-Gmail
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the development server:
```bash
python manage.py runserver
```

When you run the application for the first time you have to authorize access to your data and give permission to access and modify emails. This creates a new file "token.json" in your repo.

:no_entry:**Security** : Do not push or share "credentials.json" or "token.json" files. Major security issues.

## Features

### Inbox

Lists all of the user's unread emails. Viewed emails are muted. "Sent": lists all of users sent emails.

![Inbox](Resources/inbox.jpg)


### Mail

When clicked on an email, it displays its details. Users can reply to the mail or Mark it as read.

![Mail](Resources/mail.jpg)


### Compose

Users can send a new email.

![Composemail](Resources/compose.jpg)



### Reply mail

Users can reply to emails which takes them to compose form with recipients and subjects filled in.


![ReplyMail](Resources/replymail.jpg)
