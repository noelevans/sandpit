from stdimage                     import StdImageField

from django.db                    import models
from django.contrib.auth.models   import User
from django.utils.translation     import ugettext_lazy as _

from arts_meetup.tags.models      import *
from arts_meetup.booking.models   import *
from arts_meetup.consts.uk_places import UK_PLACES
from arts_meetup.consts.countries import COUNTRIES


class Profile(models.Model):

    # Can also add
    # help_text and verbose_name
    # Think help_name is for admin pages and
    # verbose_name is for text on templates?

    GENDERS = (('N', ''), ('M', 'Male'), ('F', 'Female'))

    PERSON, GROUP, VENUE = range(3)
    PROFILE_TYPES = ((PERSON, _('Person')),
                     (GROUP,  _('Group')),
                     (VENUE,  _('Venue')),)
    type = models.PositiveIntegerField(choices=PROFILE_TYPES, default=PERSON)

    # Generic attributes
    email             = models.EmailField()
    picture           = StdImageField(
                                upload_to='userpics/',
                                blank=True,
                                size=(200, 267, True),
                                thumbnail_size=(60, 80, True))
    city              = models.CharField(max_length=16, choices=UK_PLACES)
    country           = models.CharField(max_length=2,  choices=COUNTRIES)
    registration      = models.DateTimeField(auto_now_add=True)
    last_activity     = models.DateTimeField(auto_now=True)
    friends           = models.ManyToManyField('self', symmetrical=False, blank=True)      # Do I want to make this a friend network?
    bio               = models.CharField(max_length=1024, blank=True)
#    past_booking      = models.ManyToManyField(Booking, blank=True, related_name='old_bookings')
#    booking           = models.ManyToManyField(Booking, blank=True, related_name='bookings')

    # For Person
    user              = models.ForeignKey(User, unique=True, blank=True, null=True)
    # For all
    name              = models.CharField(max_length=32, unique=True)


    # For Person
    first_name        = models.CharField(max_length=64, blank=True)
    last_name         = models.CharField(max_length=64, blank=True)
    sex               = models.CharField(max_length=1, choices=GENDERS, blank=True)
    dob               = models.DateField(blank=True, null=True)
    role              = models.ManyToManyField(RoleTag, blank=True)     # (Job(s))
    other_tags        = models.ManyToManyField(OtherTag, blank=True)
    email_msged       = models.BooleanField("Email me when someone sends me a ArtsTent message", default=True)
    email_news        = models.BooleanField("Email me when something new is added on ArtsTent", default=False)

    # For venue
    org_name         = models.CharField("Venue's name", max_length=128, blank=True)
    address_line_1   = models.CharField(max_length=128, blank=True)
    address_line_2   = models.CharField(max_length=128, blank=True)
    postcode         = models.CharField(max_length=10, blank=True)
    telephone        = models.CharField(max_length=32, blank=True)
    contact          = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='contacts')
    producing        = models.BooleanField("Currently producing works", default=False)
    recieving        = models.BooleanField("Currently receiving works", default=False)
    venue_tags       = models.ManyToManyField(VenueTag, blank=True)

    # For Group
    # name
    # contact          = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='grp_contacts')
    group_admins     = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='grp_admin')
    group_tags       = models.ManyToManyField(GroupTag, blank=True)

    # admin
    is_valid = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # do some logic to check Profile is OK
        print "Entering save()"
        if self.type == Profile.PERSON:
            self.name = self.user.username
        # finally
        super(Profile, self).save(*args, **kwargs)
        print "Leaving save()"


    def __unicode__(self):
        return self.name


    def _get_full_name(self):
        if self.type == Profile.PERSON:
            return '%s %s' % (self.first_name, self.last_name)
        else:
            return self.org_name
    full_name = property(_get_full_name)



    # Assumed to be of format DD/MM/YYY
    def str_to_date(str_date):
        date_arr = str_date.split('/')
        return date(int(date_arr[2]), int(date_arr[1]), int(date_arr[0]))



    def add_booked_time(self, start_date, end_date, activity, b_location, b_more):

        debug = False # The real work has been moved to Booking (and must stay there)


#    def add_booked_time(self, start_date, end_date, activity, b_location, b_more):
#
#        start_arr = start_date.split('/')
#        b = Booking(
#            start=str_to_date(start_date),
#            end=str_to_date(end_date),
#            name=activity,
#            location=b_location,
#            more=b_more)
#        booking_set.add(b)      # Changed here and top of method



    # This get_absolute _url method should be used
    # with the following in url.py ...
    #
    # (r'^people/(\d+)/$', 'people.views.details'),
    #
    @models.permalink
    def get_absolute_url(self):
        return ('users.views.details', [str(self.id)])


    class Meta:

        ordering = ['-last_activity']
        # ordering = ['?']  -  random ordering
        # Profile.objects.order_by('?')

        get_latest_by = "-last_activity"




#class Project(models.Model):
#
#    name             = models.CharField(max_length=64)
#    preferred_class  = models.CharField(max_length=64)   # a "Project", "Production" or even a "idea group"
#    # free form answer but also provide defaults eg. finished, in progress, just starting
#    status           = models.CharField(max_length=128)
#    city             = models.CharField(max_length=4, choices=UK_PLACES)
#    coordinators     = models.ManyToManyField(Profile, related_name='group_coords')
#    members          = models.ManyToManyField(Profile, related_name='group_members')
#    tags             = models.ManyToManyField(ProjectTag)
#    active           = models.BooleanField()

