from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import MyForm

def send_email(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            recipient_name = form.cleaned_data['recipient_name']
            message = form.cleaned_data['message']

            # Render the email template
            email_message = render_to_string('app_name/email_template.html', {
                'recipient_name': recipient_name,
                'message': message,
            })

            # Send the email
            send_mail('Subject', email_message, 'your_email@gmail.com', [recipient_email])

            return render(request, 'app_name/success.html')
    else:
        form = MyForm()

    return render(request, 'app_name/form.html', {'form': form})
