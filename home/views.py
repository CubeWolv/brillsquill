from django.shortcuts import render
from profiles.models import Poems ,UserProfile,ImagePoem # Make sure to import your Poem model
from django.core.mail import send_mail
from django.conf import settings
from itertools import chain
from operator import attrgetter
from django.contrib import messages
from django.core.mail import EmailMessage, get_connection



def home(request):
    poems = Poems.objects.all()
    image_poems = ImagePoem.objects.all()

    # Combine the two querysets and sort them by created_on timestamp
    combined_poems = sorted(
        chain(poems, image_poems),
        key=attrgetter('created_on'),
        reverse=True
    )

    user_profiles = UserProfile.objects.all()

    context= {
        'combined_poems':combined_poems,
        'user_profiles':user_profiles
    }

    return render(request, 'home/home.html',context)


def contact(request):
    if request.method == "POST":
        subject = "New Contact Form Submission"
        email_from = request.POST.get("email")  # Use the sender's email from the form
        recipient_list = [settings.DEFAULT_FROM_EMAIL, ]  # Use a predefined email address as the recipient

        # Get additional form data
        name = request.POST.get("name")
        tel = request.POST.get("tel")

        # Modify the message to include name and tel
        message = f"Name: {name}\nTel: {tel}\n\n{request.POST.get('message')}"

        # Use the email_from variable for both EmailMessage and send_mail
        email = EmailMessage(
            subject,
            message,
            email_from,
            recipient_list,
            reply_to=[email_from],  # Set the reply-to address to the user's email
        )

        email.send()

        messages.success(request, 'Message sent.')
        print(email)

    return render(request, 'other/contact/contact.html')
