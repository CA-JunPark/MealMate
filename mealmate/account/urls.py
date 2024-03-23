from django.urls import path
from account.views import CreateAccount, Login, LogOut
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('createAccount/', CreateAccount.as_view(), name='createAccount'),
    path("logout/", LogOut.as_view(), name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
