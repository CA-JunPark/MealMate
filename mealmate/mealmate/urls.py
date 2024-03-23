from django.urls import path, include
from .views import Home
from post.views import CreatePost, PostMoreInfo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include('account.urls')),
    path('home/', Home.as_view(), name = 'home'),
    path('createPost/', CreatePost.as_view(), name = 'createPost'),
    path('postMoreInfo/', PostMoreInfo.as_view(), name='postMoreInfo'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
