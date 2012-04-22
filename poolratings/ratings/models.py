from django.db                  import models
from django.contrib.auth.models import User
from django                     import forms
from django.forms               import ModelForm

RATING_CHOICES = zip(range(5), range(5))

class Address(models.Model):
    first_line    = models.CharField(max_length=128)
    second_line   = models.CharField(max_length=128, blank=True)
    city          = models.CharField(max_length=32, blank=True)
    postcode      = models.CharField(max_length=8, blank=True)

    def __unicode__(self):
        substitutes = (self.first_line, self.second_line, self.postcode)
        return '%s %s (%s)' % substitutes


class Pool(models.Model):
    name          = models.CharField(max_length=128, unique=True)
    address       = models.ForeignKey(Address, blank=True)
    website       = models.URLField(blank=True)
    blurb         = models.TextField(blank=True)
    is_public     = models.BooleanField()
    
    def pros(self):
        pros = []
        for rating in self.rating_set.all():
            pros.extend(rating.pro_tags.all())
        return pros

    def cons(self):
        cons = []
        for rating in self.rating_set.all():
            cons.extend(rating.con_tags.all())
        return cons

    def __unicode__(self):
        return self.name


class ProTag(models.Model):
    description = models.CharField(max_length=128)

    def __unicode__(self):
        return self.description


class ConTag(models.Model):
    description = models.CharField(max_length=128)

    def __unicode__(self):
        return self.description


class Rating(models.Model):
    pool     = models.ForeignKey(Pool)
    review   = models.TextField(blank=True)
    stars    = models.IntegerField(choices=RATING_CHOICES)
    pro_tags = models.ManyToManyField(ProTag, blank=True)
    con_tags = models.ManyToManyField(ConTag, blank=True)
    name     = models.CharField(max_length=128)
    email    = models.EmailField()
    
    def __unicode__(self):
        substitutes = (self.pool, self.review, self.stars)
        return '%s: %s (%d/5)' % substitutes


class RatingForm(ModelForm):
    stars = forms.TypedChoiceField(
                    coerce=int,
                    choices=RATING_CHOICES,
                    widget=forms.RadioSelect
                )
    class Meta:
        model   = Rating
        exclude = ('pool',)
