from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect , JsonResponse
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
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse
import json
# Create your views here.

@login_required(login_url='my_login')
def index(request):
    template = 'index.html'
    income_sources = Income_sources.objects.filter(user=request.user)
    selected_income_source = None
    income_amount = None
    user = request.user
    now = timezone.now()
    last_login = user.last_login

    is_first_login = False
    if now - last_login < timedelta(minutes=1):
        is_first_login = True
    if 'income_source_id' in request.GET:
        income_source_id = request.GET['income_source_id']
        selected_income_source = Income_sources.objects.filter(id=income_source_id, user=request.user).first()
        if selected_income_source:
            income_amount = selected_income_source.amount
    
    
    monthly_expense = Monthly_Expense.objects.filter(user=request.user).first()
    selected_income = request.session.get('selected_income')
    total_income = request.session.get('total_income')
    total_expense = request.session.get('total_expense')
    context = {
        'expense_amount': monthly_expense.exp_amt if monthly_expense else None,
        'income_sources': income_sources,
        'selected_income_source': selected_income_source,
        'income_amount': income_amount,
        'is_first_login': is_first_login,
        'selected_income': selected_income,
        'total_income': total_income,
        'total_expense': total_expense
        
    }
    
    return render(request , template , context)

def register(request):

    # form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)   

        if form.is_valid():
            
            form.save()

            return redirect("my_login")
        
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

                
                return redirect('/')
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

    
        
        allert(email , date_obj , custom_text)
    return render(request , 'custom.html')
def allert(user_email , alert , custom_text):
    
     alert_date = alert - timedelta(days=5)
    
     current = timezone.now().date()
     
     if current>= alert_date.date():
            print(timezone.now().date())
        # Send the email
            subject = "Reminder: Your  due date is approaching"
            message = f"Your event of { custom_text } is coming Don't forget to prepare!"
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





            

def save_income(request):
    if request.method == 'POST':
        user = request.user
        exp_amt = request.POST.get('exp_amt')
        saving_goal = request.POST.get('saving')
        num_incomes = request.POST.get('numIncomes',0)
        Monthly_Expense.objects.create(user= user  , exp_amt = exp_amt)
        try:
            num_incomes = int(num_incomes)
        except ValueError:
            num_incomes = 0 
        for i in range(1, num_incomes+1):
            
            source = request.POST.get(f'incomeSource{i}')
            amount = request.POST.get(f'incomeAmount{i}')
            Income_sources.objects.create(user = user , source=source, amount=amount)
            
        return HttpResponseRedirect(reverse('home') + '?show_elements=true')
    
    return render(request, 'custom.html')





def update_income_amount_view(request):
    user = request.user
    income_source_id = request.GET.get('income_source_id')
    income_source = Income_sources.objects.filter(id=income_source_id, user=request.user).first()
    income_amount = income_source.amount if income_source else None
    
    expense_source = Monthly_Expense.objects.get(user=user)
    expense_amount = expense_source.exp_amt
    return JsonResponse({'income_amount': income_amount , 'expense_amount':expense_amount})



def add_transaction_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract the transaction data
        text = data.get('text')
        amount = float(data.get('amount'))
        income_source = int(data.get('income_source_id'))
        income_source = Income_sources.objects.get(id=income_source)
        transaction = Transaction.objects.create(user=request.user,income_source = income_source, text=text, amount=amount)

#         # Update balance, income, and expense
        transactions = Transaction.objects.filter(user=request.user , income_source = income_source)
        total = sum(transaction.amount for transaction in transactions)
        income = sum(transaction.amount for transaction in transactions if transaction.amount > 0)
        expense = sum(transaction.amount for transaction in transactions if transaction.amount < 0)

        return JsonResponse({
            'transaction': {
                'id': transaction.id,
                'text': transaction.text,
                'amount': transaction.amount
            },
            'balance': total,
            'income': income,
            'expense': expense
        })

    return JsonResponse({'error': 'Invalid request method'})


def init_data(request):
    user = request.user
    income_sources = Income_sources.objects.filter(user= user)
    income_source_data = [{'id': source.id ,'amount':source.amount} for source in income_sources]
    expenses = Monthly_Expense.objects.filter(user =user)
    expenses_data = [{'amount':expense.exp_amt} for expense in expenses]
    data = {
        'income_sources':income_source_data,
        'expenses':expenses_data,
    }
    return JsonResponse(data)


def updated_values(request):
    if request.method == "POST":
        data = json.loads(request.body)
        selected_income = data.get("selectedIncome")
        total_income = data.get("totalIncome")
        total_expense = data.get("totalExpense")

        # Store the updated values in the session
        request.session['selected_income'] = selected_income
        request.session['total_income'] = total_income
        request.session['total_expense'] = total_expense

        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})