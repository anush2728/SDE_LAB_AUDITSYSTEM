from django.urls import path

from . import views

urlpatterns = [
    path("",views.loginpage, name='login'),
    path("events",views.events, name='events'),
    path("home",views.home, name='home'),
    path("actmaster",views.actmaster,name='actmaster'),
    path("createnewuser",views.createnewuser, name='createnewuser'),
    path("newact",views.newact,name='newact'),
    path("logout",views.logoutpage, name='logout'),
    path('userlist',views.userlist,name='userlist'),
    #path('subcont',views.subcont,name='subcont'),
    path("upload",views.send_files,name="upload"),
    path('aud',views.aud,name='aud'),
    path('aevents/<int:pk>',views.checkevent,name='aevent'),
    path('viewprofile',views.viewprofile,name='viewprofile'),
]