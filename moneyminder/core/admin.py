from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Record)
admin.site.register(Income)
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(custom_alert)
admin.site.register(Income_sources)
admin.site.register(Monthly_Expense)
admin.site.register(Transaction)
admin.site.register(saving_goal)
admin.site.register(Customer)
admin.site.register(UserExpenseRecord)
admin.site.register(Total)