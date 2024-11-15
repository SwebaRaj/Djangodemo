from django.shortcuts import render,redirect
from shop.models import product
from cart.models import Cart
from django.contrib.auth.decorators import login_required
import razorpay
from cart.models import Payment
from cart.models import Order_details
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
@login_required
def addtocart(request,i):
    p=product.objects.get(id=i)
    u=request.user
    try:
        c=Cart.objects.get(product=p,user=u)
        if(p.stock>0):
            c.quantity+=1
            c.save()
            p.stock-=1
            p.save()
    except:
        if (p.stock > 0):
            c=Cart.objects.create(product=p,user=u,quantity=1)
            c.save()
            p.stock -= 1
            p.save()
    return redirect('cart:cart')


def cartview(request):
    u=request.user
    total=0
    c=Cart.objects.filter(user=u)
    total=0
    for i in c:
        total+=i.quantity*i.product.price

    context={'cart':c,'total':total}
    return render(request,'cart.html',context)


@login_required()
def cartremove(request,i):
    p = product.objects.get(id=i)
    u = request.user
    try:
        c = Cart.objects.get(product=p, user=u)
        if (c.quantity > 1):
            c.quantity -= 1
            c.save()
            p.stock += 1
            p.save()
        else:
            c.delete()
            p.stock+=1
            p.save()

    except:
        pass

    return redirect('cart:cart')


@login_required()
def  delete(request, i):
        p = product.objects.get(id=i)
        u = request.user
        try:
            c = Cart.objects.get(product=p, user=u)
            c.delete()
            p.stock += c.quantity
            p.save()
        except:
            pass

        return redirect('cart:cart')

def order_form(request):
    if(request.method=="POST"):
        address = request.POST['ad']
        phone = request.POST['ph']
        pin = request.POST['pi']
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.quantity*i.product.price
        total1=int(total*100)
        print(total)

        client=razorpay.Client(auth=('rzp_test_OUBbFMebBG9v0X','iNFahKsTytu2EegmLvXUgGTd'))  #creates a client connection
        #using razorpay id and secret code

        response_payment=client.order.create(dict(amount=total1,currency='INR')) #creates an order with
        #razorpay using razorpay client

        print(response_payment)
        order_id=response_payment['id']

        status=response_payment['status']

        if(status=='created'):
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o=Order_details.objects.create(pro=i.product,user=u,no_of_items=i.quantity,address=address,phone=phone,pin=pin,order_id=order_id)
                o.save()
        response_payment['name']=u.username
        context={'payment':response_payment}
        return render(request,'payment.html',context)

    return render(request,'order.html')

from django.contrib.auth import login
@csrf_exempt
def paymentstatus(request,u):
    u = User.objects.get(username=u)
    if not request.user.is_authenticated:
        login(request,u)

    if(request.method=="POST"):
        response=request.POST
        print(response)

        param_dict={
            'razorpay_order_id':response['razorpay_order_id'],
            'razorpay_payment_id':response['razorpay_payment_id'],
            'razorpay_signature':response['razorpay_signature'],

        }

         # to check the authenticity of razorpay signature

        client=razorpay.Client(auth=('rzp_test_OUBbFMebBG9v0X','iNFahKsTytu2EegmLvXUgGTd'))  #to create razorpay
        print(client)
        try:
            status = client.utility.verify_payment_signature(param_dict)   # to check the authenticity of the razorpay signature
            print(status)

            #to retrieve a perticular record from payment table matching with razorpay response order id

            p=Payment.objects.get(order_id=response['razorpay_order_id'])
            p.razorpay_payment_id=response['razorpay_payment_id']
            p.paid=True
            p.save()

            #to retrive a records from Order_details table matching with razorpay response order id

            o = Order_details.objects.filter(order_id=response['razorpay_order_id'])
            print(o)
            for i in o:
                i.payment_status = "completed"
                i.save()

            u=User.objects.get(username=u)
            c=Cart.objects.filter(user=u)
            c.delete()





        except:
            pass

    return render(request,'payment_status.html',{'status':status})

@login_required
def order_view(request):
    u = request.user
    o = Order_details.objects.filter(user=u)
    print(o)
    context = {'orders': o}
    return render(request,'orderview.html',context)

