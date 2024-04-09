from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('createPost/', CreatePost.as_view(), name='createPost'),
    path('postMoreInfo/', PostMoreInfo.as_view(), name='postMoreInfo'),
    path('myMeals/', MyMeals.as_view(), name='myMeals'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
