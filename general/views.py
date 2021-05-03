from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from smtplib import SMTPException
from django.urls import reverse
import os

def home(request):
    return render(request, 'general/home.html')

def about(request):
    return render(request, 'general/about.html')

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        customer_name = request.POST.get('name')
        customer_email = request.POST.get('email')
        customer_number = request.POST.get('number')
        customer_message = request.POST.get('message')

        if customer_name == '' or customer_email == '' or customer_number == '' or customer_message == '':
            return JsonResponse( {'status': 'error'} )

        email_contents = 'Customer name: ' + customer_name + '\n'
        email_contents += 'Customer email: ' + customer_email + '\n' 
        email_contents += 'Customer phone number: ' + customer_number + '\n'
        email_contents += 'Message from customer: ' + customer_message


        email = EmailMessage(
            subject='Customer quote request',
            body=email_contents,
            from_email=os.environ.get('EMAIL_USER'),
            to=[os.environ.get('BUSINESS_EMAIL')]
        )
        try:
            email.send()
            url = reverse('contact')
            data = {'success': url}
            messages.success(request, 'Your message has been sent sucessfully! We will get back to you as soon as possible.')
            return JsonResponse(data)

        except SMTPException as err:
            return JsonResponse( {'status': 'error'} )

    else:
        return render(request, 'general/contact.html')

    return render(request, 'general/contact.html')
