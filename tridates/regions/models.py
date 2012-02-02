from django.db     import models


class Region(models.Model):

    name = models.CharField(max_length=120)
    parent_region = models.ForeignKey('self', blank=True, null=True)

    def get_absolute_url(self):
        return "/regions/" + self.id

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ("name",)
