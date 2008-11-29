from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User


class Group(models.Model):
    
    group_type = models.CharField(max_length=50)
    
    slug = models.SlugField(_('slug'), unique=True)
    name = models.CharField(_('name'), max_length=80)
    creator = models.ForeignKey(User, related_name="created_groups", verbose_name=_('creator'))
    created = models.DateTimeField(_('created'), default=datetime.now)
    description = models.TextField(_('description'))
    members = models.ManyToManyField(User, verbose_name=_('members'))
    
    deleted = models.BooleanField(_('deleted'), default=False)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return ("group_detail", [self.group_type, self.slug])
    get_absolute_url = models.permalink(get_absolute_url)
