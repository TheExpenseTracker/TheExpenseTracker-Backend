from django.shortcuts import render , redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect , JsonResponse
from .forms import CreateUserForm, LoginForm , CustomerForm
from django.contrib.auth.models import User , auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Sum
from django.core.mail import send_mail
from datetime import timedelta , datetime
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
import json
from datetime import date
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
    # Total.objects.create(user=user , total_income = total)
    
    updated_balance = float(total) - exp_amount
    
    # selected_income = request.session.get('selected_income')
    # total_income = request.session.get('total_income')
    # total_expense = request.session.get('total_expense')
    saving_query = saving_goal.objects.filter(user = request.user)
    saving = saving_query.first()
    totalincome = Total.objects.filter(user = user).first()
    s= saving.goal if saving else None
    if s:
        saving_amount = (s/100)*totalincome.total_income
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
            Customer.objects.create(user = user , username = username , email=user.email , phone = None, profileimg=None ,info = "This is my info" ,age = 18 , location = 'Ktm,Nepal')

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
    total = Total.objects.filter(user=user).first()
    expense= Monthly_Expense.objects.filter(user=user).first()
    savinggoal = saving_goal.objects.filter(user=user).first()
    customer = Customer.objects.filter(user=user).first()
    # customer = Customer.objects.filter(user=user).first()
    # print(customer)

    # if request.method == "POST":

    #     form = CustomerForm(request.POST)   

    #     if form.is_valid():
            
    #         form.save()

    #         return redirect("home")
        
    # else:
    #     form = CustomerForm()

    context = { 'user':user , 'total':total , 'expense':expense , 'savinggoal':savinggoal , 'customer':customer}

    return render(request, 'account.html', context=context)
            
def custom(request):
   
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
def customalert(request):
    user = request.user
    
    if request.method =='POST':
        custom_text = request.POST['alertMessage']
        date = request.POST['alertDate']
        cus = custom_alert.objects.create(user=user , custom_text = custom_text , date = date)
        cus.save()
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        email = user.email

    
        
        allert(email , date_obj , custom_text)
    return render(request , 'customemi.html')

def faq(request):
    return render(request , 'faq.html')
def emialert(request):
    
    user = request.user
    if request.method == 'POST':
        date = request.POST['emiDate']
        email = user.email
        emi_alert(email , date)
    return render(request , 'emialert.html')

def emi_alert(email , date):

    today = timezone.now().date()
    today_d = today.day
    # today_day =datetime.strptime(today, '%Y-%m-%d')
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    date_day = date_obj.day
    alert_date = date_day-5
    if today_d >= alert_date:
        
        subject = "Reminder: Your  EMI paying date is approaching"
        message = f"You EMI due at approaching , Please be prepared"
        from_email = 'money.minder077@gmail.com'  # Replace with your email
        recipient_list = [email]  # Replace with the recipient's email
        send_mail(subject, message, from_email, recipient_list)
        # Send alert here
        
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
        total_amount = Income_sources.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
        print(total_amount)
        # Get or create the Total object for the user
        Total.objects.create(user=user , total_income = total_amount)

       
            
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
        iexp = Total.objects.filter (user=request.user).first()
        
        if iexp is not None:

            iexp.total_income+= float(transactions.amount) if transactions.amount > 0 else 0 
            iexp.save()
        balance = float(iexp.total_income )- mexpp.exp_amt
        svg = saving_goal.objects.filter(user = request.user ).first()
        svg_amt = iexp.total_income*(svg.goal/100.00)
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
            'income': iexp.total_income,
            'expense': mexpp.exp_amt,
            'svg_amt': svg_amt,
            # 'saving':saving.goal
        })
    
    mexp = Monthly_Expense.objects.filter(user = request.user)
    mexpp = mexp.first()
    iexp = Total.objects.filter (user=request.user).first()
    balance = float(iexp.total_income )- mexpp.exp_amt

    return JsonResponse({'balance': balance,
            'income': iexp.total_income,
            'expense': mexpp.exp_amt})

def calculator(request):
    return render(request , 'try.html')

def chupdate_values(request):


    user = request.user.id
    
    transaction = Transaction.objects.filter(user=user).order_by('created_at')
    e = [0] if not transaction.exists() else [t.amount if t.amount < 0 else 0 for t in transaction]
    i = [0] if not transaction.exists() else [float(t.amount if t.amount > 0 else 0) for t in transaction]
    c = [] if not transaction.exists() else [t.created_at.strftime('%Y-%m-%d') for t in transaction]
    te = [] if not transaction.exists() else [t.text for t in transaction]
            
            

    context = {
        'e':e,
        'i':i,
        'c':c,
        'te':te,
    }
    return JsonResponse(context)
        
def remove_transaction(request, transaction_id):
    
        try:
            transaction = Transaction.objects.get(user=request.user, pk=transaction_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Transaction not found")
        total_expense = Monthly_Expense.objects.filter(user=request.user).first()
        total_income = Total.objects.filter(user=request.user).first()


        if transaction.amount < 0:
            # Subtract from expenses
            if total_expense:
                print("*"*100)
                print(transaction.amount)
                total_expense.exp_amt -= abs(float(transaction.amount))
                total_expense.save()
        if transaction.amount > 0:
            # Subtract from income
            if total_income:
                total_income.total_income -= float(transaction.amount)
                total_income.save()
        balance = 0
        if total_income and total_expense:
            balance = total_income.total_income - total_expense.exp_amt
        
        # Delete the transaction
        transaction.delete()

        # Get the updated transactions
        transactions = Transaction.objects.filter(user=request.user).values()

        return JsonResponse({
            'income' : total_income.total_income,
            'expense' : total_expense.exp_amt,
            'balance' : balance,
        })
  

def upload(request):
    if request.method=="POST":
        customer = Customer.objects.get(user=request.user)
        customer.profileimg = request.FILES['profile_picture']
        customer.save()
        return HttpResponseRedirect('/account')  # Redirect to the account page
    return render(request, 'account.html')  # Render the account page initially

def save_data(request):
    user = request.user
    customer = Customer.objects.filter(user=user).first()
    if request.method=="POST":
        key = request.POST.get('key')
        value = request.POST.get('value')
        if key == 'email':
            user.email = value
            user.save()
        elif key =='location':
            customer.location = value
            customer.save()
        elif key =='age':
            customer.age = value
            customer.save()
        elif key =='age':
            customer.age = value
            customer.save()
        elif key =='about':
            customer.info = value
            customer.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
        

def get_history(request):
    user = request.user
    history = Transaction.objects.filter(user=user, created_at__gte=date.today())
    data = [{"id":data.id, "text":data.text, "amount":data.amount} for data in history]
    return JsonResponse(data=data, safe=False, status=200)