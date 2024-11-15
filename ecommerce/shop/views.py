from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from shop.models import Categories,product
from django.contrib.auth import login,authenticate

def categories(request):
    c=Categories.objects.all()
    context={'categories':c}
    return render(request,'categories.html',context)

def products(request,p):        #here p recive the category id
    print(p)
    k = Categories.objects.get(id=p)     # Reads a perticular object using id
    p=product.objects.filter(category=k)   #read all product under a perticular category object
    context = {'categories': k,'products':p}
    return render(request,'products.html',context)


def productdetails(request,p):
    pro=product.objects.get(id=p)
    context={'product':pro}
    return render(request, 'productdetails.html',context)
def register(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        f = request.POST['f']
        l = request.POST['l']
        e = request.POST['e']
        if (p == cp):
            u = User.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l)
            u.save()
            return redirect('shop:categories')
        else:
            return HttpResponse('password are not same')
    return render(request,'register.html')

def user_login(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        user = authenticate(username=u, password=p)
        if user:  # if matching user exist
            login(request, user)
            return redirect('shop:categories')
        else:  # if no matching user
            return HttpResponse("invalid credentials")

    return render(request,'login.html')

def user_logout(request):
    user_logout(request)
    return redirect('shop:login')

def addcategory(request):
    if(request.method == 'POST'):
        na = request.POST['na']
        i = request.FILES['i']
        de = request.POST['de']
        c=Categories.objects.create(name=na,image=i,description=de)
        c.save()
        return redirect('shop:categories')
    return render(request,'addcategory.html')



def addproduct(request):
    if(request.method == 'POST'):
        na = request.POST['na']
        i = request.FILES['i']
        de = request.POST['de']
        s = request.POST['s']
        pp = request.POST['pp']
        c = request.POST['cat']
        cat=Categories.objects.get(name=c)

        p=product.objects.create(name=na,image=i,desc=de,stock=s,price=pp,category=cat)
        p.save()
        return redirect('shop:categories')

    return render(request,'addproduct.html')

def addstock(request,p):
    p=product.objects.get(id=p)

    if(request.method=='POST'):
        p.stock=request.POST['ad']
        p.save()
        return redirect('shop:categories')

    context={'pro':p}
    return render(request,'addstock.html',context)