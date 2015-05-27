from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from services.views import ItemViewSet

# django admin
admin.autodiscover()


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'items', ItemViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/',include(router.urls)),
    url(r'^api-auth/',include('rest_framework.urls', namespace='rest_framework')),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

