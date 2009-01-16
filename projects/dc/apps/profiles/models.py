from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from timezones.fields import TimeZoneField

from tagging.fields import TagField



class Profile(models.Model):
    
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    name = models.CharField(_('name'), max_length=50, null=True, blank=True)    
    location = models.CharField(_('location'), max_length=40, null=True, blank=True)
    website = models.URLField(_('Website'), null=True, blank=True, verify_exists=False)    
    job_description = models.TextField(_('Job Description'), null=True, blank=True)
    work_done = models.TextField(_("Work I've done"), null=True, blank=True)
    work_doing_now = models.TextField(_("Work I'm doing now"), null=True, blank=True)
    awards = models.TextField(_('My Awards'), null=True, blank=True)
    certifications = models.TextField(_('My Certifications'), null=True, blank=True)    
    about = models.TextField(_('About Me'), null=True, blank=True)    
    
    tags = TagField()
    
    def __unicode__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return ('profile_detail', None, {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)
    
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)
