from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from prefectcrm import settings
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from django import conf
from kingadmin.sites import site

print('sites',site.enabled_admins)
from kingadmin import app_setup

app_setup.kingadmin_auto_disever()
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
            return redirect(request.GET.get('next','/kingadmin/'))
        else:
            error_msg =' wrong username or password!'
    return render(request, 'kingadmin/login.html',{'error_msg':error_msg})

def acc_logout(request):
    return redirect('/login/')
def app_index(request):

    return render(request,'kingadmin/app_index.html',{'site':site})
@login_required


def get_filter_result(request,querysets):

    filter_conditions = {}
    for key,val in request.GET.items():

        if key in  ('_page','0'):continue
        if val:

             filter_conditions[key] = val
    return querysets.filter(**filter_conditions),filter_conditions

def get_orderby_result(request,querysets,admin_class):
    '''排序'''

    orderby_index = request.GET.get('_o')
    if orderby_index:
        orderby_key =admin_class.list_display[int(orderby_index)]
        return querysets.order_by(orderby_key)
    else:
        return querysets

@login_required
def table_obj_list(request,app_name,model_name):

    '''取出指定model的数据返回前端'''
    #print('app_name,model_name',site.enabled_admins[app_name][model_name])
    admin_class =site.enabled_admins[app_name][model_name]
    querysets = admin_class.model.objects.all()
    querysets ,filter_conditions =get_filter_result(request,querysets)
    admin_class.filter_condtions = filter_conditions
    #sorted querysets
    querysets =get_orderby_result(request,querysets,admin_class)


    paginator = Paginator(querysets,2)
    page = request.GET.get('_page')

    try:
        querysets =paginator.page(page)
    except PageNotAnInteger:
        querysets = paginator.page(1)
    except EmptyPage:
        querysets= paginator.page(paginator.num_pages)


    print(request.GET)
    return render(request,'kingadmin/table_obj_list.html',{'querysets':querysets,'admin_class':admin_class})

