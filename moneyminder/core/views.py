from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.views import View
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User , auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import send_mail
from datetime import timedelta , datetime
from django.utils import timezone


# Create your views here.

@login_required(login_url='my_login')
def index(request):
    template = 'index.html'
    
    return render(request , template)

def register(request):

    # form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)   

        if form.is_valid():
            
            form.save()

            return redirect("info")
        
    else:
        form = CreateUserForm()

    context = {'Form':form}

    return render(request, 'signup.html', context=context)

def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)


            if user is not None:

                auth.login(request,user)

                return redirect("home")
    context = {'loginForm':form}


    return render(request, 'signin.html', context=context)
@login_required(login_url='my_login')
def info (request):
    user = request.user
    category = Category.objects.earliest('created_at')
    if request.method == 'POST':
        income = request.POST['income']
        expense = request.POST['expense']
        saving_goal = request.POST['saving_goal']
        inc = Income.objects.create(user = user , income = income , saving_goal = saving_goal)
        inc.save()
        exp = Expense.objects.create(user = user , ex_amount = expense , category = category , remark = 'First' , bill_image = None , payment_method = 0)
        exp.save()
        return redirect('home')
    return render(request , 'info.html')



        
def custom(request):
    user = request.user
    if request.method =='POST':
        custom_text = request.POST['custom_text']
        date = request.POST['custom_date']
        cus = custom_alert.objects.create(user=user , custom_text = custom_text , date = date)
        cus.save()
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        email = user.email
    
        
        allert(email , date_obj)
    return render(request , 'custom.html')
def allert(user_email , alert):
     alert_date = alert - timedelta(days=5)
     current = timezone.now().date()
     
     if current>= alert_date.date():
            print(timezone.now().date())
        # Send the email
            subject = "Reminder: Your payment due date is approaching"
            message = f"Your event of  Don't forget to prepare!"
            from_email = "sakarbhandari100000@gmail.com"  # Replace with your email
            recipient_list = [user_email]  # Replace with the recipient's email
            send_mail(subject, message, from_email, recipient_list)





# def saving_alert(user_email , saving_goal):
#     # user = Profile.objects.all()
#     subject = "Saving Goal Alert"
#     message = f"Your Saving goal os {saving_goal} is approaching, You need to spend less"
#     from_email = '077bct032.sakar@sagarmatha.edu.np'
#     recipient_list = [user_email]
#     send_mail(subject, message, from_email, recipient_list)
# def saving_goal_status(userinfo):
#     saving_target = userinfo.saving_goals
#     if saving_target<100:
#         saving_alert(userinfo.user.email, userinfo.saving_goals)




