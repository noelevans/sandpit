from django.db import models
from django.contrib.auth.models import User

from arts_meetup.users.models     import *

# When making a Message object. Must always call make_copies() to
# maintain integrity after all recipients are added
class Message(models.Model):

    # These 3 are ones which generally should be
    # filled when making a Message object
    sender    = models.ForeignKey(Profile, related_name='poster')
    recipient = models.ManyToManyField(Profile, related_name='receiver')
    body      = models.TextField()
    # Internal cogs of Message class
    is_public = models.BooleanField(default=False)
    owner     = models.ForeignKey(Profile, related_name='msg_owner')
    sent_time = models.DateTimeField(auto_now_add=True)
    reply_to  = models.ForeignKey('Message', blank=True, null=True)
    is_valid  = models.BooleanField(default=True)

    class Meta:
        ordering = ('-sent_time',)

#    def __unicode__(self):
#        return "" + sender

    def _is_public(self):
        return is_public

    def save(self, *args, **kwargs):
        try:
            self.owner
        except:
            self.owner = self.sender
        super(Message, self).save(*args, **kwargs)

    # Must always be called after last recipient has been added to Message
    def make_copies(self, *args, **kwargs):
        # set owner as recipient for each new message
        for r in self.recipient.all():
            m = Message(
                    is_public = self.is_public,
                    owner = r,
                    sender = self.sender,
                    body = self.body
                )
            m.save()
            m.recipient = self.recipient.all()
