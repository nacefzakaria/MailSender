import pandas as pd
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string

class Command(BaseCommand):
    help = 'Send bulk emails to recipients from a data sheet'

    def handle(self, *args, **options):
        # Load your data from the CSV or Excel file
        data = pd.read_csv('test.csv')  # Replace with your file path

        # Iterate over the rows and send emails
        for _, row in data.iterrows():
            recipient_email = row['Email']  # Replace 'email_column' with the actual column name
            recipient_name = row['First name']  # Replace 'name_column' with the actual column name
            message = "row['message_column']"  # Replace 'message_column' with the actual column name

            # Render the email template
            email_message = render_to_string('ITmail/recrutement.html', {
                'recipient_name': recipient_name,
                'message': message,
            })

            # Send the email
            send_mail('Subject', email_message, 'nacefzakaria8@gmail.com', [recipient_email])

        self.stdout.write(self.style.SUCCESS('Bulk emails sent successfully'))
