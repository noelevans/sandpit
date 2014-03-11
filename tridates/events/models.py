import datetime

from django.db                   import models
from django.contrib.auth.models  import User
from tridates.regions.models     import Region
from tridates.disciplines.models import Discipline


class Event(models.Model):

    STATUS_CHOICES = (
        ('B', 'Individual entrant & charity positions'), 
        ('C', 'Charity positions only'),
        ('N', 'Non-charity positions only'),
        ('F', 'No positions available'),
        ('U', 'Unknown'),
    )
    
    name = models.CharField(max_length=120)
    start_date = models.DateField()
    duration = models.IntegerField()
    disciplines = models.ManyToManyField(Discipline, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    region = models.ForeignKey(Region)
    website = models.URLField(null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(User, related_name='event added by')
    confirmed_by = models.ForeignKey(User, related_name='event confirmed by', null=True, blank=True)
    date_confirmed = models.DateField(null=True, blank=True)
    locked = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    description = models.TextField(null=True, blank=True)

    def get_end_date(self):
        print type(self.start_date)
        duration_timedelta = datetime.timedelta(days=self.duration-1)
        return self.start_date + duration_timedelta
        
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ("start_date",)

