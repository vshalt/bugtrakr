from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def get_user_roles(request):
    return request.user, [role for role in request.user.profile.roles]

def send_email(subject, text_content, html_content, from_email, to):
    msg = EmailMultiAlternatives(subject=subject, body=text_content,
                                 from_email=from_email, to=to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_ticket_update_email(link, profile, ticket):
    if ticket.assigned.user.email in settings.DEMO_ACCOUNTS:
        return
    txt = get_template('tickets/mail/update.txt')
    html = get_template('tickets/mail/update.html')
    d = {'link': link, 'profile': profile, 'ticket': ticket}
    subject = 'Ticket updated'
    from_email = settings.EMAIL_USER
    to = ticket.assigned_user.user.email
    text_content = txt.render(d)
    html_content = html.render(d)
    send_email(subject, text_content, html_content, from_email, [to])


def send_ticket_assign_email(request, user, ticket):
    if ticket.assigned_user.user.email in settings.DEMO_ACCOUNTS:
        return
    txt = get_template('tickets/mail/assign.txt')
    html = get_template('tickets/mail/assign.html')
    link = request.build_absolute_uri(ticket.get_absolute_url())
    d = {'request': request, 'link': link, 'user': user, 'ticket': ticket}
    subject = 'Ticket assigned'
    from_email = settings.EMAIL_USER
    to = ticket.assigned_user.user.email
    text_content = txt.render(d)
    html_content = html.render(d)
    send_email(subject, text_content, html_content, from_email, [to])


def send_comment_create_email(request, comment, ticket):
    if ticket.assigned_user:
        if ticket.assigned_user.user.email in settings.DEMO_ACCOUNTS:
            return
        txt = get_template('tickets/mail/comment.txt')
        html = get_template('tickets/mail/comment.html')
        link = request.build_absolute_uri(ticket.get_absolute_url())
        d = {'link': link, 'ticket': ticket, 'comment': comment}
        subject = 'Comment posted'
        from_email = settings.EMAIL_USER
        to = ticket.assigned_user.user.email
        text_content = txt.render(d)
        html_content = html.render(d)
        send_email(subject, text_content, html_content, from_email, [to])
