from django.urls import path
from . views import LoginView,SignUpView,LogoutView,csrf_token,Whoami

urlpatterns=[
    path('login/',LoginView.as_view(),name='login'),
    path('signup/',SignUpView.as_view(),name='signup'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('csrf_token/',csrf_token,name='csrf_token'),
    path('whoami/',Whoami.as_view(),name='whoami'),


]