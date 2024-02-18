import random

from django.core.mail import send_mail
from django.conf import settings

def get_code():
    code = str()
    for _ in range(4):
        num = random.randint(0,9)
        code+=str(num)
    return code


def sending_email(email_subject, email_body, email_to):
    send_mail(
        email_subject,
        email_body,
        'no-reply@dignitech.com',
        [email_to],
        fail_silently=True,
    )



def sending_code(random_code, email_to):
    email_subject = 'Verification Code'
    email_body = 'Below is the verification code:\n{}'.format(random_code)
    email_to = email_to
    sending_email(email_subject, email_body, email_to)


def sending_invite(email_to):
    email_subject = 'Invitation for Trend game'
    email_body = """
        Ciao,

        sono, ti volevo invitare a partecipare ad una campagna GameTour su trend, una app innovatva che ti permette di guadagnare premi fantastici partecipando a delle challanges.

        Per scoprire di più visita il sito web oppure scarica l'app.

        Ti avviso che è in corso un evento ed a breve le iscrizioni termineranno ! Non perdere l'occasione, vieni a scoprire di cosa sto parlando ! 
        ----
        Object: Invito Trend """
    email_to = email_to
    sending_email(email_subject, email_body, email_to)
