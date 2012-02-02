import string

from django.shortcuts               import get_object_or_404
from django.views.generic           import list_detail
from django.contrib.auth.models     import User
from django.shortcuts               import render_to_response
from django.template                import RequestContext
from django.contrib.auth.decorators import login_required
from django.http                    import *
from django.core.mail               import send_mass_mail

from arts_meetup.messaging.models   import *

@login_required
def msgs_by_user(request, username):
    user = get_object_or_404(User, username__iexact=username)
    if request.user.username != user.username:
        return HttpResponseForbidden(
            "Oi! Whad'ya think this is, a post office? Read yer own post. 403")
    return list_detail.object_list(
        request,
        queryset = Message.objects.filter(owner=user.get_profile()),
        template_name = 'messaging/msgs_by_user.html',
        template_object_name = 'message',
        extra_context = {
            'h_user':   user,
            'can_show': True,
            'all_tags': Tag.objects.all(),
        }
    )


def email_notify(sender, recipients, msg):

    def f(recip):
        email = User.objects.get(username=recip).email
        inbox = 'http://www.artstent.com/msging/' + recip + '/'
        return (
            "You've been found on ArtsTent",
            # "http://www.artstent.com/users/" + sender.user.username + "/" + \
            sender.user.username + \
            " has sent you a message on ArtsTent:\n\n" + \
            msg + \
            "\n\nFollow this link to view your messages " + inbox,
            'no-reply@artstent.com',
            [email]
          )
    email_recips = filter(
            lambda u: User.objects.get(username=u).get_profile().email_msged,
            recipients
        )
    datatuple =  map(f, email_recips)
    send_mass_mail(datatuple)


# details can be recipients /
@login_required
def create_msg(request):

    errors = []
    recipients = request.GET.getlist('contact')

    if request.method == 'POST':
        recipients = request.POST.get('recipients', '')
        if not recipients:
            errors.append('Enter recipicent(s)')
        recip_list = recipients.replace(',', ' ').split()
        for r in recip_list:
            try:
                User.objects.get(username=r)
            except User.DoesNotExist:
                errors.append('Not a valid user: ' + str(r))
        if not errors:
            public = True
            if request.POST.get('private', 'off') == 'on':
                public = False
            m = Message(
                sender=request.user.get_profile(),
                body=request.POST.get('body', ''))
            m.save()
            for r in recip_list:
                m.recipient.add(Profile.objects.get(user__username=r))
            m.make_copies()
            email_notify(
                    sender = request.user.get_profile(),
                    recipients = recip_list,
                    msg = request.POST.get('body', '')
                )
            return HttpResponseRedirect('/msging/'+request.user.username+'/')

    return render_to_response(
            'messaging/create_msg.html',
            {
                'init_recipients': string.join(recipients, ', '),
                'all_tags': Tag.objects.all()
            },
            RequestContext(request))


def delete_msg(request, id):
    # Have both person calling; request.user and id
    owner = Message.objects.get(id=id).owner.user
    req_user = request.user
    if owner != req_user:
        return HttpResponseForbidden(
            "You are not authenticated as the correct user to perform this operation")
    Message.objects.get(id=id).delete()
    return HttpResponseRedirect('/msging/'+request.user.get_profile().name+'/')
