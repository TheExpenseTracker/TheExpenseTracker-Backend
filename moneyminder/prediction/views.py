# views.py
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .predictionLogic import calculate_percentage_spent
import json


@login_required
def prediction(request):
    context = {}
    current_user = request.user
    if request.method == 'POST':
        data = json.loads(request.body)
        entered_amount = data.get('amount', 0)  # Convert to float
        
        if entered_amount < 0:
            current_user = request.user
            print(f"Entered Amount: {entered_amount}")
            entered_amount = abs(entered_amount)
            message = calculate_percentage_spent(entered_amount, current_user)
            # messages.success(request, message)
            context = {
                        'message': message                        
                    }
    return JsonResponse(context)
