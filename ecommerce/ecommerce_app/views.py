from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from .models import category,Product
from  django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User,auth

# Create your views here.
def home(request):
    return HttpResponse("hai")

def allProduCat(request,c_slug=None):
    c_page=None
    products_list=None
    if c_slug!=None:
        c_page=get_object_or_404(category,slug=c_slug)
        products_list=Product.objects.filter(category=c_page,available=True)
    else:
        products_list=Product.objects.all().filter(available=True)
    paginator=Paginator(products_list,8)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        products=paginator.page(page)
    except(EmptyPage,InvalidPage):
        products=paginator.page(paginator.num_pages)
    return render(request,'category.html',{'category':c_page,'products':products})

def ProdCatDetail(request,c_slug,product_slug):
    try:
        product=Product.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'product':product})

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('ecommerce_app:allProdCat')
        else:
            messages.info(request,'invalid details')
            return redirect('ecommerce_app:allProdCat')
    else:
        return render(request,"login.html")

def register(request):
    if request.method=="POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1==password2:
             if User.objects.filter(username=username).exists():
                 messages.info(request,"username taken")
                 return redirect('ecommerce_app:register')
             elif User.objects.filter(email=email).exists():
                 messages.info(request,"email taken")
                 return redirect('ecommerce_app:register')
             else:
                  user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name,last_name=last_name)
                  user.save();
                  print("user created")
                  return redirect('ecommerce_app:allProdCat')

        else:
            print("password not match")
            return redirect('ecommerce_app:allProdCat')
    else:
          return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('ecommerce_app:allProdCat')