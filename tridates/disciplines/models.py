from django.db import models


class Discipline(models.Model):

    name = models.CharField(max_length=120)
    description = models.TextField(null=True)
    parent_discipline = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return self.name
