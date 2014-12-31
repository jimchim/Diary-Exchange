from django.conf.urls import patterns, url


from diary import views

urlpatterns = patterns('',
	url(r'^$', views.index, name = 'index'),
	url(r'^login/$', views.login, name = 'login'),
	url(r'^logout/$', views.logout, name = 'logout'),
	url(r'^entry/new/$', views.new_entry, name = 'new_entry'),
	url(r'^entry/(?P<entry_id>\d+)/$', views.entry, name = 'entry'),
	url(r'^entry/(?P<entry_id>\d+)/(?P<slug>[-\w]+)/$', views.entry, name = 'entry_slug'),
	url(r'^entry/edit/(?P<entry_id>\d+)/$', views.entry_edit, name = 'entry_edit'),
	url(r'^entry/edit/(?P<entry_id>\d+)/(?P<slug>[-\w]+)/$', views.entry_edit, name = 'entry_edit_slug'),
	#url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name = 'results'),
)