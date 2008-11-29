from django.conf.urls.defaults import *

group_config = {
    "a": {
        "list_template_name": "groups/a_list.html",
        "create_template_name": "groups/a_create.html",
        "detail_template_name": "groups/a_detail.html",
    },
    "b": {
        
    },
    "c": {
        
    }
}

urlpatterns = \
    patterns('',
        url(r'^list/(\w+)/$', 'groups.views.group_list', {"group_config": group_config}, name="group_list"),
        url(r'^create/(\w+)/$', 'groups.views.group_create', {"group_config": group_config}, name="group_create"),
        url(r'^your/(\w+)/$', 'groups.views.your_groups', {"group_config": group_config}, name="your_groups"),
        
        # @@@ don't like this URL pattern
        url(r'^detail/(\w+)/(\w+)$', 'groups.views.group_detail', {"group_config": group_config}, name="group_detail"),
        
#        url(r'^tribe/(\w+)/delete/$', 'tribes.views.delete', name="tribe_delete"),
    )