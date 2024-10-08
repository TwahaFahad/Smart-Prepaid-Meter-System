from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout
from django.contrib import messages

from .utils import auth_user_should_not_access
from .forms import UserLoginForm

# Create your views here.

@auth_user_should_not_access
def loginView(request):

    next_url = request.GET.get('next', '/')

    form = UserLoginForm(request.POST or None)
    msg = None
    next_url = request.GET.get('next', '/')

    if request.method == 'POST':
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            print(phone_number, password)
            user = authenticate(phone_number=phone_number, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect(request.POST.get('next', '/')) 
            else: 
                messages.warning(request, 'invalid credetials')
                return redirect('login')
        else:
            msg = 'error validating form'
    context = {
        'next': next_url,
        'form': form,
        'msg': msg
    }
    return render(request, 'accounts/login.html', context)


def logoutView(request):
    logout(request)
    return redirect('accounts:login')
