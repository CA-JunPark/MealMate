from django.urls import path, include
from .views import Home
from account.views import CreateAccount, Login
from post.views import CreatePost, PostMoreInfo

urlpatterns = [
    path('', Login.as_view(), name = 'login'),
    path('createAccount/', CreateAccount.as_view(), name = 'createAccount'),
    path('home/', Home.as_view(), name = 'home'),
    path('createPost/', CreatePost.as_view(), name = 'createPost'),
    path('postMoreInfo/', PostMoreInfo.as_view(), name='postMoreInfo'),
]
