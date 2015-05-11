from django.db                import models
from django.utils.translation import ugettext_lazy as _

from arts_meetup.users.models import *
class Tag(models.Model):

    MAX_TAGS = 10

    name             = models.CharField(primary_key=True, max_length=32, unique=True)
    description      = models.CharField(max_length=128, blank=True)
    # eg so Hereford will be a child to Midlands
    children         = models.ManyToManyField("self", blank=True)
    is_valid         = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# eg. Ballerina, Director
class RoleTag(Tag):

    def __unicode__(self):
        return self.name

class VenueTag(Tag):

    def __unicode__(self):
        return self.name

class GroupTag(Tag):

    def __unicode__(self):
        return self.name

class BookingTag(Tag):

    def __unicode__(self):
        return self.name


class OtherTag(Tag):

    PERSON, GROUP, VENUE = range(3)
    PROFILE_TYPES = ((PERSON, _('Person')),
                     (GROUP,  _('Group')),
                     (VENUE,  _('Venue')),)
    type = models.PositiveIntegerField(choices=PROFILE_TYPES, default=PERSON)

