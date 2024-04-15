from django.shortcuts import render,redirect
from django.views import View
from .models import Product,Customer,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
 def get(self,request):
  saree=Product.objects.filter(category='S')
  lehanga=Product.objects.filter(category='L')
  gharara=Product.objects.filter(category='G')
  cape=Product.objects.filter(category='C')
  return render(request,'app/home.html',{'sarees':saree,'lehangas':lehanga,'ghararas':gharara,'capes':cape})
  

class ProductDetailView(View):
 def get(self,request,pk):
  product = Product.objects.get(pk=pk)
  item_already_in_cart=False
  if request.user.is_authenticated:
    item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
 user=request.user
 product_id = request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart_products = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        
        if cart_products:
            for cart_product in cart_products:
                temp_amount = cart_product.quantity * cart_product.product.discounted_price
                amount += temp_amount
            
            total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart_products, 'total_amount': total_amount, 'amount': amount})
        else:
            return render(request, 'app/emptycart.html')
    else:
        return render(request, 'app/emptycart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def plus_cart(request):
  if request.method=='GET':
    prod_id = request.GET['prod_id']
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount=0.0
    shipping_amount=70.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    data=None
    for p in cart_product:
      tempamount=(p.quantity*p.product.discounted_price)
      amount+=tempamount

    data={
    'quantity':c.quantity,
    'amount':amount,
    'totalamount':amount+shipping_amount
    }
    return JsonResponse(data)
  

def minus_cart(request):
    if request.method=='GET':
        prod_id = request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        data=None
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount

        data={
        'quantity':c.quantity,
        'amount':amount,
        'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

def remove_cart(request):  
  if request.method=='GET':
    prod_id = request.GET['prod_id']
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount=0.0
    shipping_amount=70.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    data=None
    for p in cart_product:
        tempamount=(p.quantity*p.product.discounted_price)
        amount+=tempamount
    data={
    'amount':amount,
    'totalamount':amount+shipping_amount
    }
    return JsonResponse(data)

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
 def get(self,request):
  form=CustomerProfileForm()
  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
 
 @login_required
 def post(self,request):
  form=CustomerProfileForm(request.POST)
  if form.is_valid():
   user=request.user
   name=form.cleaned_data['name']
   locality=form.cleaned_data['locality']
   city=form.cleaned_data['city']
   state=form.cleaned_data['state']
   zipcode=form.cleaned_data['zipcode']
   reg=Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
   reg.save()
   messages.success(request,'Congratulations!! Profile Updatd Succssfully')
  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
 op=OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':op})



def sari(request,data=None):
 if data == None:
  saris = Product.objects.filter(category='S')
 else:
  saris=Product.objects.filter(category='S')
 return render(request, 'app/cape.html',{'saris':saris})

def lehanga(request,data=None):
 if data == None:
  saris = Product.objects.filter(category='L')
 else:
  saris=Product.objects.filter(category='L')
 return render(request, 'app/cape.html',{'saris':saris})

def cape(request,data=None):
 if data == None:
  saris = Product.objects.filter(category='C')
 else:
  saris=Product.objects.filter(category='C')
 return render(request, 'app/cape.html',{'saris':saris})

def gharara(request,data=None):
 if data == None:
  saris = Product.objects.filter(category='G')
 else:
  saris=Product.objects.filter(category='G')
 return render(request, 'app/cape.html',{'saris':saris})

class CustomerRegistrationView(View):
 def get(self,request):
  form=CustomerRegistrationForm()
  return render(request,'app/customerregistration.html',{'form':form})
 
 def post(self,request):
  form=CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,'Congratulations!! Registered Successfully')
   form.save()
  return render(request,'app/customerregistration.html',{'form':form})
  
# @login_required
# def user_logout(request):
#     logout(request)
#     return render(request, 'app/logout.html', {})

  
@login_required
def checkout(request):
 user=request.user
 add=Customer.objects.filter(user=user)
 cart_items=Cart.objects.filter(user=user)
 amount=0.0
 shpping_amount=70
 cart_product = [p for p in Cart.objects.all() if p.user==request.user]
 data=None 
 totalamount=None
 if cart_product:
    for p in cart_product:
        tempamount=(p.quantity*p.product.discounted_price)
        amount+=tempamount
    totalamount=amount+shpping_amount
 return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
  user=request.user
  custid=request.GET.get('custid')
  customer=Customer.objects.get(id=custid)
  cart=Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
    c.delete()
  return redirect('orders')
