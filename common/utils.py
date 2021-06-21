from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def get_user_roles(request):
    return request.user, [role for role in request.user.profile.roles]


def send_ticket_update_email(profile, ticket):
    txt = get_template('tickets/mail.txt')
    html = get_template('tickets/mail.html')
    d = Context({})
    subject = 'Ticket updated'
    from_email = settings.EMAIL_USER
    to = ticket.assigned_user.email
    text_content = txt.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(subject=subject, text_content=text_content,
                                 from_email=from_email, to=[to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
