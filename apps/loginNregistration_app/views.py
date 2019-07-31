from django.shortcuts import render, HttpResponse, redirect
from .models import Registration
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request,"loginNregistration_app/index.html")

def register(request):
    errors = Registration.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print("*************************", hash1)
        Registration.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'], birthday=request.POST['birthday'],email=request.POST['email'],password=hash1)
        user = Registration.objects.last()
        request.session['user_id'] = user.id
        return redirect('/success')

def login(request):
        user_list = Registration.objects.filter(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(),           user_list[0].password.encode()):
            request.session['user_id'] = user_list[0].id
            return redirect('/success')  
        # else:
        #     message.error(request, "Invalid credentials!!!")
        #     return redirect('/') 
        else:
            errors = Registration.objects.login_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user=Registration.objects.get(id=request.session['user_id'])
        context = {
            'user':user,
        }
        messages.error(request, "Successfuly registered!!!!")
        return render(request,"loginNregistration_app/success.html", context)

def logout(request):
    request.session.clear()
    messages.error(request, "Please Log In")
    return redirect('/')