from django.conf.urls.defaults import *



urlpatterns = patterns('',

    url(r'^$', 'proto_search.views.search_form', name="search_form"),
    
)
