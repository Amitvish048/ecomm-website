import random
import razorpay
from django.shortcuts import render,redirect,HttpResponse
from .models import Cart, product,Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail

# Create your views here.
def home(request):
    context={}
    products=product.objects.all() #this function fetches all the records from the product table
    context['products']=products
    
    return render(request,'index.html',context)

def viewproduct(request , pid):
    context={}
    products = product.objects.get(id = pid)
    context['products'] = products
    return render(request,'product.html',context)

def catfilter(request,cid):
    products = product.objects.filter(category = cid)
    context = {}
    context['products'] = products
    return render(request,'index.html',context)

def sort(request,sid):
    context = {}
    if sid == "1":
        products = product.objects.all().order_by('price')
    elif sid == "0":
        products = product.objects.all().order_by('-price')
    context['products'] = products
    return render(request,'index.html',context)


def registration(request):
    context={}
    if(request.method=='POST'):
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        if(uname=='' or upass=='' or ucpass==''):
            context['error']='Please fill in all the details'
            return render(request,'registration.html',context)
        elif(upass!=ucpass):
            context['error']='Password and confirm password should be the same!'
            return render(request,'registration.html',context)
        else:
            user_obj= User.objects.create(password=upass,username=uname,email=uname)
            user_obj.set_password(upass) 
            user_obj.save()
            context['success']="User registered successully"
            return render(request,'registration.html',context)
    else:
        return render(request,'registration.html')
                                                               #create quiry i modelname.object.create(values)
                                                                                #.save()
                                                                                #imporrt django.contri
                                                                                #django have inbulid user table its consist of password username email
    

def user_login(request):
    context={}
    if(request.method=='POST'):
        uname= request.POST['uname']
        upass = request.POST['upass']
        if(uname=='' or upass==''):
            context['error']='Please fill all the fields'
            return render(request,'Login.html',context)
        u= authenticate(username=uname, password=upass)
        if u is not None:
            
            login(request,u)
            return redirect('/')
        else:
            context['error']='Invalid username or password'
            return render(request,'Login.html',context)
    else:
        return render(request,'Login.html')
    
def user_logout(request):
    logout(request)
    return redirect("/")

def addtocart(request,pid):
    
    if(request.user.is_authenticated):
        uid= request.user.id
        u= User.objects.get(id=uid)
        p= product.objects.get(id=pid)
        c = Cart.objects.create(uid=u, pid=p)
        c.save()

        return redirect('/')
    else:
        return redirect('/Login')

def viewcart(request):
    context ={}
    user = request.user.id
    c = Cart.objects.filter(uid = user)
    np = len(c)
    sum = 0
    for i in c:
        sum = sum + i.pid.price*i.quantity
    context['np'] = np
    context['price'] = sum
    context['products'] = c
    
    return render(request,'cart.html',context)

def removeFromCart(request,cid):
    Cart.objects.get(id = cid).delete()
    return redirect(request,'/cart.html')

def updateqty(request,qv,cid):
    if request.user.is_authenticated:
        c = Cart.objects.filter(id = cid)
        if qv == "1":
            t = c[0].quantity+1
            c.update(quantity = t)
        elif qv == "0":
            if c[0].quantity>1:
                t = c[0].quantity-1
                c.update(quantity = t)
            elif c[0].quantity == 1:
                c.delete()
        return redirect('/viewcart')
    else:
        return redirect('/login')
    

# def search(request):
#         if "q" in request.GET:
#             q = request.GET["q"]
#             data = product.objects.filter(name__icontains= q)
#         else:
#             data = product.objects.all()
#             context = {'data' : data}
#         return render(request,'templates/index.html',context)
    
# def placeorder(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user.id
        c = Cart.objects.filter(id=user)
        oid = random.randrange(1000,9999)
        for i in c:
            o = Order.create(order_id=oid,uid=user,pid=i.pid,qunatity = i.qunatity)
            o.save()
            i.delete()
        orders = Order.objects.filter(uid = user)
        
        np = len(orders)
        sum = 0
        for i in c:
            sum = sum + i.pid*i.qunatity
        context['price'] = sum
        context['np'] = np
        context['products'] = orders
    else:
        redirect("/login")
    return render(request,'placeorder.html',context)

# def placeorder(request):
    if request.user.is_authenticated:
        user = request.user
        c=Cart.objects.filter(uid=user)
        order_id = random.randrange(1000,9999)
        for i in c:
            o=Order.objects.create(order_id=order_id,uid=user,pid=i.pid,quantity=i.quantity)
            o.save()
            i.delete()
        orders = Order.objects.filter(uid=user)
        np=len(orders)
        sum=0
        for i in orders:
            sum=sum+i.pid.price*i.quantity
        context={}
        context['products']=orders 
        context['sum']=sum
        context['np']=np 
        return render(request,"placeorder.html",context)
    

def placeorder(request):
    if request.user.is_authenticated:
        user = request.user
        c = Cart.objects.filter(uid=user)
        order_id = random.randrange(1000, 9999)

        for cart_item in c:
            order, created = Order.objects.get_or_create(
                order_id=order_id, uid=user, pid=cart_item.pid, defaults={'quantity': cart_item.quantity}
            )

            if not created:
                order.quantity += cart_item.quantity
                order.save()

            cart_item.delete()

        orders = Order.objects.filter(uid=user)
        np = len(orders)
        total_sum = sum(order.pid.price * order.quantity for order in orders)

        context = {
            'products': orders,
            'sum': total_sum,
            'np': np
        }

        return render(request, "placeorder.html", context)
    
    # Return an appropriate response if the user is not authenticated
    return HttpResponse("User not authenticated")



def range(request):
    
    if(request.method == 'POST'):
        context = {}

        min_value = request.POST['min']
        max_value = request.POST['max']

        products = product.objects.filter(price__gte=min_value,price__lte=max_value)
        context['products'] = products
        return render(request,"index.html",context)
    else:
       return render(request,"index.html")


def senduseremail(request):
    msg = "payment is succ"
    send_mail(
    "EKcart Order",
    msg,
    "vishwkarmamit1708@gmail.com",
    ["vishwkarmamit1708@gmail.com"],
    fail_silently=False,
    )
    print("email")
    return redirect("/")







# import uuid
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from razorpay import Client

# from .models import Cart, Order

# def place_order(request):
#     if request.user.is_authenticated:
#         user = request.user
#         c = Cart.objects.filter(uid=user)
#         order_id = uuid.uuid4().hex[:8]

#         # Assuming you have a function to calculate total_sum
#         total_sum = calculate_total_sum(c)

#         # Create an order with the calculated total
#         order = Order.objects.create(order_id=order_id, uid=user, total_amount=total_sum)
        
#         # Initialize Razorpay client with your API key and secret
#         razorpay_client = Client(auth=("rzp_test_96Z24vMDhZdMqV", "4jYsYDnTLb14giLL9PB7foGm"))

#         # Create a Razorpay order
#         razorpay_order = razorpay_client.order.create({
#             'amount': int(total_sum * 100),  # Amount in paise (1 Rupee = 100 paise)
#             'currency': 'INR',  # Change this to your currency code
#             'payment_capture': 1  # Auto-capture payments
#         })

#         # Store the Razorpay order ID in your Django Order model
#         order.razorpay_order_id = razorpay_order['id']
#         order.save()

#         context = {
#             'order': order,
#             'razorpay_order_id': razorpay_order['id'],
#             'razorpay_key': 'your_api_key',  # Pass your Razorpay API key to the template
#         }

#         return render(request, "payment.html", context)
#     else:
#         return redirect('login')  # Redirect to the login page if the user is not authenticated

# def calculate_total_sum(cart_items):
#     # Calculate total sum based on your cart items
#     # Modify this function according to your cart and product models
#     total_sum = sum(item.pid.price * item.quantity for item in cart_items)
#     return total_sum
from decimal import Decimal

def pay(request):
    # Retrieve user's orders
    orders = Order.objects.filter(uid=request.user.id)
    total_amount = Decimal(0)

    # Calculate the total amount
    for order_item in orders:
        total_amount += Decimal(order_item.pid.price) * order_item.quantity

    # Multiply by 100 outside the loop
    total_amount *= 100

    # Create Razorpay payment order
    client = razorpay.Client(auth=("rzp_test_96Z24vMDhZdMqV", "4jYsYDnTLb14giLL9PB7foGm"))
    data = {"amount": int(total_amount), "currency": "INR", "receipt": order_item.order_id}

    try:
        payment = client.order.create(data=data)

        # Clear the user's cart after successful payment
        for order_item in orders:
            order_item.delete()

        context = {"payment": payment}
        return render(request, "pay.html", context)

    except Exception as e:
        # Handle the exception, log it, and inform the user
        print(f"Error creating Razorpay payment: {e}")
        # Redirect to an error page
        return redirect("error_page")