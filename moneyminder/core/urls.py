
from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.index, name='home'),
    path('signup',views.register, name='signup'),
    path('signin',views.my_login, name='my_login'),
    path('info',views.info, name='info'),
    path('custom',views.custom, name='custom'),
]
