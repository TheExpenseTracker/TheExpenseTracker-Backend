from datetime import datetime, timedelta
from django.db import models
from .predictor import LinearRegressionPredictor
from core.models import  Income, UserExpenseRecord
import os
from core.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.middleware import get_user

model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "linear_regression_model.joblib")
def get_current_logged_in_user():
    user = get_user(None)
    return user if isinstance(user, get_user_model()) else AnonymousUser()
def get_day_of_month():
    current_date = datetime.now()
    day_of_month = current_date.day
    return day_of_month

#extract amount from frontend
def calculate_percentage_spent(entered_amount, current_user):
    # current_date = datetime.now()
    # start_date = datetime(current_date.year, current_date.month, 1)
    # end_date = start_date.replace(day=1, month=start_date.month + 1) - timedelta(days=1)

    # # Retrieve UserExpenseRecord entries for the current user and month
    # user_expense_records = UserExpenseRecord.objects.filter(
    #     user=current_user,
    #     date__range=[start_date, end_date]
    # )

    # # Calculate the cumulative sum of total_expense_on_date
    # amount_db = user_expense_records.aggregate(total_expense=models.Sum('total_expense_on_date'))['total_expense']
    e = Monthly_Expense.objects.filter(user = current_user).first()
    # i = Income_sources.objects.filter(user = request.user)

    amount_db = e.exp_amt
    message = ""
    c_amount= abs(entered_amount) + amount_db
    # saving_goal = Income.objects.get(user=current_user).saving_goal
    sg = saving_goal.objects.filter(user = current_user).first()
    totalincome = Total.objects.filter(user = current_user).first()
    income__amount = Income_sources.objects.filter(user=current_user)
    total = sum(p.amount for p in income__amount)
    saving_amount = (sg.goal/100)*totalincome.total_income
    saving_goals = saving_amount
    #calculate percentage
    percent_spent = c_amount/ saving_goals * 100
    print(f"percent_spent: {percent_spent}")
    day = get_day_of_month()
    prediction = None
    #logic to trigger model
    if percent_spent > 50 :
        predictor = LinearRegressionPredictor(model_path)
        prediction = predictor.predict(16)
    print(f"prediction: {prediction}")
    #logic to decide message
    if prediction:
        ActualVsPre = percent_spent - prediction
        if ActualVsPre > 5 :
            # prevDiff = UserExpenseRecord.objects.get(id=1).actual_vs_pre
            prevDiff = 3
            if prevDiff > ActualVsPre :
                message = 'Bravo! you are doing better. Lets get more closer to our goal'
            else:
                message = 'You are getting further far from your goal. You need to control you spending amount'
        else:
            message = 'Wow you are rocking this goal. Keep saving'
    else:
        ActualVsPre = 0
        message = None
#code to display a div banner for above message
    print(f"message: {message}")
    return message



#extract day of the month





