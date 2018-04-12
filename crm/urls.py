from django.conf.urls import url

from crm import views

urlpatterns = [

    url(r'^$', views.dashboard, name='sales_dashboard'),
    url(r'^customers/$', views.customer_list,name='custmoer_list'),



]