from django.db                import models
from datetime                 import date

from arts_meetup.users.models import *

def uk_date(date):
    return str(date.day) + '/' + str(date.month) + '/' + str(date.year)



class Booking(models.Model):

    profile          = models.ForeignKey('users.Profile')
    start            = models.DateField()
    end              = models.DateField()
    name             = models.CharField(blank=True, max_length=64)
    location         = models.CharField(blank=True, max_length=128)
    more             = models.TextField(blank=True)
    c_date           = models.DateTimeField(auto_now_add=True)
    m_date           = models.DateTimeField(auto_now=True)
    # from Project class
    preferred_class  = models.CharField(max_length=64, blank=True)   # a "Project", "Production" or even a "idea group"
    tags             = models.ManyToManyField(BookingTag, blank=True)
    is_valid         = models.BooleanField(default=True)

    class Meta:
        ordering = ['start']

    def __unicode__(self):

        display_name = ''
        if self.name:
            display_name = self.name
        return '"' + display_name + '": ' + uk_date(self.start) + ' -> ' + uk_date(self.end)


    # todo noel
    def add_booked_time(self, start_date, end_date, activity, b_location, b_more):
        debug = False



"""
Sole purpose is to help make analysis of when user is next
free (and subsequent to that). This shadows the above Bookings.
When two Bookings overlap, this just shows the aggregated time
excluded for the profile. This willbe reset whenever they
delete a Booking and regenerated
"""
class MetaBooking(models.Model):

    profile          = models.ForeignKey('users.Profile')
    start            = models.DateField()
    end              = models.DateField()
    c_date           = models.DateTimeField(auto_now_add=True)
    m_date           = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start']



#        start_arr = start_date.split('/')
#        b = Booking(
#            start=str_to_date(start_date),
#            end=str_to_date(end_date),
#            name=activity,
#            location=b_location,
#            more=b_more)
#        booking_set.add(b)      # Changed here and top of method

#class FreeSpace(models.Model):
#
#    profile          = models.ForeignKey('users.Profile')
#    start            = models.DateField()
#    end              = models.DateField()
#    name             = models.CharField(blank=True, max_length=64)
#    location         = models.CharField(blank=True, max_length=128)
#    more             = models.CharField(blank=True, max_length=131072)
#    c_date           = models.DateTimeField(auto_now_add=True)
#    m_date           = models.DateTimeField(auto_now=True)
#    # from Project class
#    preferred_class  = models.CharField(max_length=64, blank=True)   # a "Project", "Production" or even a "idea group"
#    tags             = models.ManyToManyField(BookingTag, blank=True)
#    is_valid         = models.BooleanField(default=True)
#
#    class Meta:
#        ordering = ['start']


#class Itinerary(models.Model):
#
#
#    # this is an object to contain Bookings
#
#    def __unicode__(self):
#        return self.booking_set.all()
#
#
#    def next_free_slot(self):
#        nothing = ''
#
#    def is_currently_busy(self):
#        today = date.today()
#        bs = self.booking_set
#        if 0 == bs.count:
#            return False
#        return 0 != len(
#            bs.filter(start__lte=today).filter(end__gte=today))
#    #is_currently_free = property(_is_currently_free)
#
#
#
#    # But need to order this so they are sorted by
#    # end date before doing [0:3] operation
#    def _next_three(self):
#        return self.booking_set.filter(end__gte=date.today()).order_by('start')[0:3]
