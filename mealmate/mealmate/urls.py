from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', Home.as_view(), name = 'home'),
    path('searchPost/', searchPost, name="searchPost"),
    path("", include('account.urls')),
    path("post/", include('post.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
