from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
def test(request):
    return HttpResponse('hehe')