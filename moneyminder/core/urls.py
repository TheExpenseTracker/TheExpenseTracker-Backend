
from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.index, name='home'),
    path('signup',views.register, name='signup'),
    path('signin',views.my_login, name='my_login'),
    path('info',views.info, name='info'),
    path('custom',views.custom, name='custom'),
    path('save_income/', views.save_income, name='save_income'),
    path('update_income_amount/', views.update_income_amount_view, name='update_income_amount'),
    path('transaction/', views.add_transaction_view, name='transaction'),
    path('initial_data/', views.init_data, name='initialize_data'),
    path('updated_values/', views.updated_values, name='update_values'),
]
