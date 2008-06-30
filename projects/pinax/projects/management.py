from django.dispatch import dispatcher
from django.db.models import signals

from django.utils.translation import ugettext_noop as _

try:
    from notification import models as notification
    
    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("projects_new_member", _("New Project Member"), _("a project you are a member of has a new member"), default=1)
        notification.create_notice_type("projects_added_as_member", _("Added to Project"), _("you have been added to a project"), default=2)
        
        notification.create_notice_type("projects_new_topic", _("New Project Topic Started"), _("a new topic has started in a project you're a member of"), default=2)
        notification.create_notice_type("projects_topic_response", _("Response To Your Project Topic"), _("someone has responded on a project topic you started"), default=2)
    
    dispatcher.connect(create_notice_types, signal=signals.post_syncdb, sender=notification)
except ImportError:
    print "Skipping creation of NoticeTypes as notification app not found"
