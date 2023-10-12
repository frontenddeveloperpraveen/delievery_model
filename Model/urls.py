from django.contrib import admin
from . import views
from django.urls import path,include

urlpatterns = [
    path('',views.Home,name='Home'),
    path('query',views.Gen,name='Query'),
    path('merchant/qr',views.space,name='space'),
    path('validate/<orderid>',views.validate,name='validate'),
    path('handshake/confirmation',views.confirm,name='ok'),
]
