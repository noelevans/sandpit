from django.db                    import models
from django.utils.translation     import ugettext_lazy as _

from arts_meetup.users.models     import Profile


class URL(models.Model):

    IDENTITY, PERFORMANCES, OTHER1, OTHER2 = range(4)
    URL_TYPES = ((IDENTITY,      _('Identity')),
                 (PERFORMANCES,  _('Performances')),
                 (OTHER1,        _('Other1')),
                 (OTHER2,        _('Other2')),)
    type = models.PositiveIntegerField(choices=URL_TYPES, default=IDENTITY)

    name             = models.CharField(max_length=64)
    other_profile    = models.URLField()
    user             = models.ForeignKey(Profile)
    is_valid         = models.BooleanField(default=True)
