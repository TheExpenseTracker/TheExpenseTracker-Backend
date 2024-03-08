
from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.index, name='home'),
    path('signup',views.register, name='signup'),
    path('signin',views.my_login, name='my_login'),
    
    path('custom',views.custom, name='custom'),
    path('save_income/', views.save_income, name='save_income'),
    path('transaction/', views.add_transaction_view, name='transaction'),
    path('update_chvalues/', views.chupdate_values, name='updated_values'),
    path('remove_transaction/<int:transaction_id>/', views.remove_transaction, name='remove_transaction'),
    path('calculator', views.calculator, name='calculator'),
    path('logout', views.logout , name="logout"),
    path('account', views.account , name="account"),
    path('customalert', views.customalert , name="customalert"),
    path('emialert', views.emialert , name="emialert"),
    path('faq', views.faq , name="faq"),
    path('upload/', views.upload, name='upload'),
    path('save_data/', views.save_data, name='save_data'),
    path('ccc/', views.update_values, name='ccc'),
    path('history/', views.get_history, name="history"),
    # path('ccc/', views.ccc, name='ccc'),
]
