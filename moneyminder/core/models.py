from django.db import models
from django.core.validators import MaxValueValidator , MinValueValidator
from django.contrib.auth.models import User
# Create your models here.
class TimeStampModel(models.Model):
    """Inherit from this class to add timestamp fields in the model class"""

    created_at = models.DateTimeField(auto_now_add=True)
    """datetime: date on which the instance is created."""
    updated_at = models.DateTimeField(auto_now=True)
    """datetime: date on which the instance is updated."""
    
    class Meta:
        abstract = True
class Record(TimeStampModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete= models.CASCADE,related_name='user_record')
    
    def __str__(self) -> str:
        return self.name
    
class Income(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    income = models.FloatField()
    saving_goal = models.DecimalField(max_digits = 5 ,
                                        decimal_places=2 ,
                                        validators=[MinValueValidator(0) , MaxValueValidator(100)],
                                        help_text = 'Enter Percentage Between 0 and 100', default = None )

class Category(TimeStampModel):
    name = models.CharField(max_length=100)

    
    def __str__(self) -> str:
        return self.name

class Expense(TimeStampModel):
    METHOD = (
        (0,"Cash"),
        (1,"Online")
    )
    ex_amount = models.FloatField()
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    category = models.ForeignKey(Category , on_delete = models.CASCADE)
    remark = models.CharField(max_length=250)
    bill_image = models.ImageField(upload_to='', null=True , blank= True)
    payment_method = models.IntegerField(choices=METHOD, default=0)

    def __str__(self) -> str:
        return f'{self.category}/{self.ex_amount}'
    

class custom_alert(TimeStampModel):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    custom_text = models.CharField(max_length = 200)
    date = models.DateField()



class Income_sources(TimeStampModel):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    source = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.source


class Monthly_Expense(TimeStampModel):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    exp_amt = models.FloatField()


class Transaction(TimeStampModel):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    text = models.CharField(max_length = 255)
    amount = models.DecimalField(max_digits = 10 , decimal_places = 2)
    # created_at = models.DateTimeField(auto_now_add=True , default = None)

    def __str__(self):
        return self.text
    
class saving_goal(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    goal = models.FloatField()


class Customer(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    phone = models.IntegerField(null =True , blank = True)
    username = models.CharField(max_length = 100 , default = None)
    email = models.EmailField(default = None)
    profileimg = models.ImageField(null=True, blank=True, default='profile.jpg')
    date_created = models.DateTimeField(auto_now_add = True , null=True)
    location = models.CharField(max_length = 100 , default = 'Ktm , Nepal')
    age = models.IntegerField(default = 18)
    info = models.TextField(default = 'This is my about section')

    def __str__self(self):
        return self.user.username
    
class UserExpenseRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    total_expense_on_date = models.FloatField()
    actual_vs_pre = models.FloatField()

    def __str__(self) -> str:
        return f'{self.user.username} - {self.date}'

    class Meta:
        unique_together = ['user', 'date']


class Total(models.Model):
    user = models.ForeignKey(User,  on_delete = models.CASCADE)
    total_income = models.FloatField()
    