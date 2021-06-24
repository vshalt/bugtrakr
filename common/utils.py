from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def get_user_roles(request):
    return request.user, [role for role in request.user.profile.roles]


def send_ticket_update_email(profile, ticket, assigned):
    txt = get_template('tickets/mail/update.txt')
    html = get_template('tickets/mail/update.html')
    d = {'profile': profile, 'ticket': ticket, 'assigned': assigned}
    subject = 'Ticket updated'
    from_email = settings.EMAIL_USER
    to = ticket.assigned_user.user.email
    text_content = txt.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(subject=subject, body=text_content,
                                 from_email=from_email, to=[to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_ticket_assign_email(user, ticket):
    # txt = get_template('tickets/mail/assign.txt')
    # html = get_template('tickets/mail/assign.html')
    # d = {'profile': profile, 'ticket': ticket, 'assigned': assigned}
    # subject = 'Ticket updated'
    # from_email = settings.EMAIL_USER
    # to = ticket.assigned_user.user.email
    # text_content = txt.render(d)
    # html_content = html.render(d)
    # msg = EmailMultiAlternatives(subject=subject, body=text_content,
    #                              from_email=from_email, to=[to])
    # msg.attach_alternative(html_content, 'text/html')
    # msg.send()
    pass
