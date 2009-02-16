from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageModel
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from tagging.fields import TagField

from django.utils.translation import ugettext_lazy as _

PUBLISH_CHOICES = (
    (1, _('Public')),
    (2, _('Private')),
)

class PhotoSet(models.Model):
    """
    A set of photos
    """
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'))
    publish_type = models.IntegerField(_('publish_type'), choices=PUBLISH_CHOICES, default=1)
    tags = TagField()

    class Meta:
        verbose_name = _('photo set')
        verbose_name_plural = _('photo sets')

class Photo(ImageModel):
    """
    A photo with its details
    """
    SAFETY_LEVEL = (
        (1, _('Safe')),
        (2, _('Not Safe')),
    )

    crop_horz_choices = (
       (0, 'left'),
       (1, 'center'),
       (2, 'right'),
     )
    crop_vert_choices = (
      (0, 'top'),
      (1, 'center'),
      (2, 'bottom'),
    )
    image = models.ImageField(_('image'), upload_to='images')
    view_count = models.IntegerField(default=0)
    crop_horz = models.PositiveIntegerField(_('crop horizontal'),
                             choices=crop_horz_choices,default=1)
    crop_vert = models.PositiveIntegerField(_('crop vertical'),
                            choices=crop_vert_choices, default=1)
    title = models.CharField(_('title'), max_length=200)
    title_slug = models.SlugField(_('slug'))
    caption = models.TextField(_('caption'), blank=True)
    date_added = models.DateTimeField(_('date added'), default=datetime.now, editable=False)
    is_public = models.BooleanField(_('is public'), default=True, help_text=_('Public photographs will be displayed in the default views.'))
    member = models.ForeignKey(User, related_name="added_photos", blank=True, null=True)
    safetylevel = models.IntegerField(_('safetylevel'), choices=SAFETY_LEVEL, default=1)
    photoset = models.ManyToManyField(PhotoSet, verbose_name=_('photo set'))
    tags = TagField()

    class IKOptions:
        spec_module = 'photos.specs'
        save_count_as = 'view_count'
        cache_dir = 'photos'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ("photo_details", [self.pk])
    get_absolute_url = models.permalink(get_absolute_url)

class Pool(models.Model):
    """
    model for a photo to be applied to an object
    """

    photo           = models.ForeignKey(Photo)
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField()
    content_object  = generic.GenericForeignKey()
    created_at      = models.DateTimeField(_('created_at'), default=datetime.now)

    class Meta:
        # Enforce unique associations per object
        unique_together = (('photo', 'content_type', 'object_id'),)
        verbose_name = _('pool')
        verbose_name_plural = _('pools')
