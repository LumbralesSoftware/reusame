from django.conf.urls import patterns, include, url
from django.contrib import admin

# django admin
admin.autodiscover()

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/',include(router.urls)),
    url(r'^api-auth/',include('rest_framework.urls', namespace='rest_framework')),
)
