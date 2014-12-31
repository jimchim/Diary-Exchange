from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'diaryexchange.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('diary.urls', namespace = 'diary')),    
    url(r'^admin/', include(admin.site.urls)),
)
