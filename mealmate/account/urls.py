from django.urls import path
from account.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('createAccount/', CreateAccount.as_view(), name='createAccount'),
    path("logout/", LogOut.as_view(), name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
    path('otherProfile/', OtherProfile.as_view(), name='other')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
