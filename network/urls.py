from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from blog.views import Registration


urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', Registration.as_view(), name='registration'),
    path('', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
