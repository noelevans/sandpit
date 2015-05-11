from django.db import models

from arts_meetup.users.models     import *


class Post(models.Model):

    body     = models.CharField(max_length=512)
    author   = models.ForeignKey(Profile)
    c_time   = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def __unicode__(self):
        return self.body

    class Meta:
        ordering = ('-c_time',)

