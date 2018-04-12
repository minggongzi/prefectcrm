from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
# Create your views here.
def acc_login(request):
    error_msg =''
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            print('验证通过',user)
            login(request,user)
            return redirect(request.GET.get('next','/crm'))
        else:
            error_msg =' wrong username or password!'
    return render(request, 'login.html',{'error_msg':error_msg})

def acc_logout(request):
    return redirect('/login/')