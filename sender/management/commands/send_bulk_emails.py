import pandas as pd
import os
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.utils.safestring import mark_safe
class Command(BaseCommand):
    help = 'Send bulk emails to recipients from a data sheet'
    
    def handle(self, *args, **options):
        # Load your data from the CSV or Excel file
        data = pd.read_csv('sender/emails.csv')  # Replace with your file path
        timer = 1
        attachment = 'nacef_zakariacv.pdf'
        message = "10h30"
        # Iterate over the rows and send emails
        for _, row in data.iterrows():
            recipient_email = row['Email'] 
            recipient_name = row['name']
            Entreprise_name= row['Entrepise'] 
            Entreprise_interit= row['Entreprise_interit'] # Replace 'name_column' with the actual column name
            if timer % 6 == 0:
                hour = int(message[0:2])
                minute = int(message[3:5])
                if minute == 55:
                    hour += 1
                    minute = 00
                else:
                    minute += 5
                formatted_hour = f'{hour:02}'
                formatted_minute = f'{minute:02}'
                message = f'{formatted_hour}h{formatted_minute}'
            timer += 1

                # Load the email template
            template = loader.get_template('mails/recrutement.html')  # Replace 'app_name' with the correct app name

                # Create a context with data to render the template
            context = {
                    'recipient_name': recipient_name,
                    'appointment_time': message, 
                     'Entreprise_name' : Entreprise_name,
                     'Entreprise_interit': Entreprise_interit
                }
            # Render the email template with the context
            email_message = template.render(context)

            # Create an EmailMultiAlternatives object for sending HTML email
            subject = "Demande d'informations sur les opportunités de stage chez " + Entreprise_name
            from_email = 'chakra.hs.business@gmail.com'
            to = [recipient_email]

            msg = EmailMultiAlternatives(subject, '', from_email, to)
            msg.attach_alternative(email_message, "text/html")
            with open(attachment, 'rb') as file:
                msg.attach(os.path.basename(attachment), file.read(), 'application/pdf')

            print("sending email to " + recipient_email)
            print(recipient_name)
            print(message)
            print("###############################################")
            # Send the email
            msg.send()
        self.stdout.write(self.style.SUCCESS('Bulk emails sent successfully'))
