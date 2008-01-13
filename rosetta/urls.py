from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
urlpatterns = patterns('',
    url(r'^$', 'rosetta.views.home', name='rosetta-home'),
    url(r'^pick/$', 'rosetta.views.list_languages', name='rosetta-pick-file'),
    url(r'^select/(?P<langid>\w+)/(?P<idx>\d+)/$','rosetta.views.lang_sel', name='rosetta-language-selection'),
)
