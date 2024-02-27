from django.shortcuts import render , redirect

from django.http import HttpResponseRedirect , JsonResponse
from django.views import View
from .forms import CreateUserForm, LoginForm , CustomerForm
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
    
    user = request.user
    now = timezone.now()
    last_login = user.date_joined

    is_first_login = False
    if now - last_login < timedelta(minutes=2):
        is_first_login = True
    
    
    
    monthly_expense_queryset = Monthly_Expense.objects.filter(user=request.user)
    monthly_expense = monthly_expense_queryset.first()
    income__amount = Income_sources.objects.filter(user=request.user)
    exp_amount = monthly_expense.exp_amt if monthly_expense else 0
    total = sum(p.amount for p in income__amount)
    
    updated_balance = float(total) - exp_amount
    
    # selected_income = request.session.get('selected_income')
    # total_income = request.session.get('total_income')
    # total_expense = request.session.get('total_expense')
    saving_query = saving_goal.objects.filter(user = request.user)
    saving = saving_query.first()
    s= saving.goal if saving else None
    if s:
        saving_amount = (s/100)*float(total)
    else :
        saving_amount=0

    transactions = Transaction.objects.filter(user = user).order_by('created_at')

    context = {
        
        'income_sources': income_sources,
        'total':total,
        'updated_balance':updated_balance,
        'exp_amount':exp_amount,
        'is_first_login': is_first_login,
        # 'selected_income': selected_income,
        # 'total_income': total_income,
        # 'total_expense': total_expense,
        'saving_amount':saving_amount,
        'transactions':transactions
        # 'updated_balance' :updated_balance,
        
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
            Customer.objects.create(user = user , username = username , email=user.email , phone = None, profileimg=None , )

            if user is not None:
                # # custom alert section
                # custom_alert_query = custom_alert.objects.filter(user = request.user)
                # custom = custom_alert_query.all()
                # if custom:
                #     for customs in custom:
                #         customs_alert = customs.custom_text
                #         customs_date = customs.date
                #         email = user.email
                #         # date_obj = datetime.strptime(customs_date, "%Y-%m-%d")
                #         allert_contd(email , customs_date , customs_alert)


                

                auth.login(request,user)

                
                return redirect('/')
    context = {'loginForm':form}


    return render(request, 'signin.html', context=context)

@login_required(login_url = 'my_signin')
def logout(request):
    auth.logout(request)
    return redirect('my_login')

def account(request):
    user= request.user
    customer = Customer.objects.filter(user=user).first()
    print(customer)

    if request.method == "POST":

        form = CustomerForm(request.POST)   

        if form.is_valid():
            
            form.save()

            return redirect("home")
        
    else:
        form = CustomerForm()

    context = {'Form':form , 'customer':customer}

    return render(request, 'account.html', context=context)
            
def custom(request):
    user = request.user
    
    if request.method =='POST':
        custom_text = request.POST['alertMessage']
        date = request.POST['alertDate']
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
            subject = "Reminder!!!!: Your  due date is approaching"
            message = f"Your event of { custom_text } is approaching in 5 days. Start Preparing!!!"
            from_email = "money.minder077@gmail.com"  # Replace with your email
            recipient_list = [user_email]  # Replace with the recipient's email
            send_mail(subject, message, from_email, recipient_list)


def allert_contd(user_email , alert , custom_text):
    
     alert_date = alert - timedelta(days=5)
    
     current = timezone.now().date()
     
     if current>= alert_date:
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
        t = Monthly_Expense.objects.filter(user=user)
        u = Income_sources.objects.filter(user=user)
        v = saving_goal.objects.filter(user=user)
        if t.exists():
            t.delete()
        if u.exists():
            u.delete()
        if v.exists():
            v.delete()
            
        exp_amt = request.POST.get('exp_amt')
        saving_goals = request.POST.get('saving_goal')
        num_incomes = request.POST.get('numIncomes',0)
        Monthly_Expense.objects.create(user= user  , exp_amt = exp_amt)
        saving_goal.objects.create(user= user , goal = saving_goals)
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



def update_values(request):
    user = request.user
    count = count_sources_for_user(user)
    m=Monthly_Expense.objects.get(user=user)
    c = m.exp_amt
    d = saving_goal.objects.get(user = user)
    # for i in range(1,count+1):  
    #     s = Income_sources.objects.get(user=user)
        
    #     i=i+1
    #     return render(request , 'update.html',{'count':count,'c':c , 'd':d , 's':s})

    return render(request , 'update.html',{'count':count,'c':c , 'd':d})


def count_sources_for_user(user):
    
    sources_count = Income_sources.objects.filter(user=user).count()
    return sources_count
# def update_income_amount_view(request):
#     user = request.user
#     income_source_id = request.GET.get('income_source_id')
#     income_source = Income_sources.objects.filter(id=income_source_id, user=request.user).first()
#     income_amount = income_source.amount if income_source else None
    
#     expense_source = Monthly_Expense.objects.get(user=user)
#     expense_amount = expense_source.exp_amt
#     return JsonResponse({'income_amount': income_amount , 'expense_amount':expense_amount})



def add_transaction_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract the transaction data
        text = data.get('text')
        amount = float(data.get('amount'))
        
        transaction = Transaction.objects.create(user=request.user, text=text, amount=amount)

#         # Update balance, income, and expense
        transactions = Transaction.objects.filter(user=request.user).order_by('-created_at').first()
       
        mexp = Monthly_Expense.objects.filter(user = request.user)
        mexpp = mexp.first()
        if mexpp is None:
    # Create a new MonthlyExpense object if it doesn't exist for the user
            mexpp = Monthly_Expense(user=request.user)
            mexpp.save()
        mexpp.exp_amt += float(abs(transactions.amount)) if transactions.amount < 0 else 0 
        mexpp.save()
        iexp = Income_sources.objects.filter(user=request.user).first()
        

        iexp.amount+= transactions.amount if transactions.amount > 0 else 0 
        iexp.save()
        balance = float(iexp.amount )- mexpp.exp_amt
        # saving = saving_goal.objects.filter(user=request.user).first()
        # savi = (saving.goal/100)* float(iexp.amount)
        # saving.goal = (savi/float(iexp.amount))
        # saving.save()
        


        return JsonResponse({
            'transaction': {
                'id': transaction.id,
                'text': transaction.text,
                'amount': transaction.amount
            },
            'balance': balance,
            'income': iexp.amount,
            'expense': mexpp.exp_amt,
            # 'saving':saving.goal
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
    

def calculator(request):
    return render(request , 'try.html')

def chupdate_values(request):
    e=[]
    i=[]
    c=[]
    te=[]

    user = request.user
    
    transaction = Transaction.objects.filter(user=user).order_by('created_at')
    if not transaction.exists():
        e = [0]
        i = [0]
        c = []
        te = []
    else:
        for t in transaction:
            es = t.amount if t.amount< 0 else 0
            e.append(es)
            
            
            ic = float(t.amount if t.amount> 0 else 0)
            i.append(ic)

            cr = t.created_at
            
            
            c.append(cr)

            tex = t.text
            te.append(tex)

            
            

    context = {
        'e':e,
        'i':i,
        'c':c,
        'te':te,
    }
    return JsonResponse(context)
        
    