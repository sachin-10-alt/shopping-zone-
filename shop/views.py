
from django.db.models import Q
from .models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import redirect, render
from shop.form import CustomUserForm
from .models import * 
from .models import Order
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

def home(request):
    products=Product.objects.filter(trending=1)
    return render (request, "shop/index.html",{"products":products})

def cart_page(request):
    if request.user.is_authenticated:
       cart=Cart.objects.filter(user=request.user)
       return render(request,"shop/cart.html",{"cart":cart})
    else:
       return redirect("/login")
    
def remove_cart(request,cid):
        if request.user.is_authenticated:
            cartitem=Cart.objects.get(id=cid, user=request.user)
            cartitem.delete()
            return redirect("/cart")  
        else:
            return redirect("/login")
@csrf_exempt
def add_to_cart(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_qty = data['product_qty']
            product_id = data['pid']
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id, product_id=product_id).exists():
                    return JsonResponse({'status': 'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                        return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product Stock Not Available'}, status=404)
            else:
                return JsonResponse({'status': 'Product Not Found'}, status=404)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=401)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)

@csrf_exempt
def buy_now(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_qty = data['product_qty']
            product_id = data['pid']
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if product_status.quantity >= product_qty:
                    # Create an order
                    Order.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                    return JsonResponse({'status': 'Order Placed'}, status=200)
                else:
                    return JsonResponse({'status': 'Product Stock Not Available'}, status=404)
            else:
                return JsonResponse({'status': 'Product Not Found'}, status=404)
        else:
            return JsonResponse({'status': 'Login to Buy Now'}, status=401)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)


def order_summary(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "shop/order_summary.html", {"orders": orders})

@csrf_exempt
def place_order(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_qty = data['product_qty']
            product_id = data['pid']
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if product_status.quantity >= product_qty:
                    # Create an order
                    Order.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                    return JsonResponse({'status': 'Order Placed'}, status=200)
                else:
                    return JsonResponse({'status': 'Product Stock Not Available'}, status=404)
            else:
                return JsonResponse({'status': 'Product Not Found'}, status=404)
        else:
            return JsonResponse({'status': 'Login to Place Order'}, status=401)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)

@login_required
def remove_order(request, oid):
    try:
        order = Order.objects.get(id=oid, user=request.user)
        order.delete()
        messages.success(request, "Order removed successfully")
    except Order.DoesNotExist:
        messages.error(request, "Order not found")
    return redirect('order_summary')

def logout_page(request):
   if request.user.is_authenticated:
    logout(request)
    messages.success(request,"logout in successfully")
   return redirect("/")


def login_page(request):
    if request.user.is_authenticated:
       return redirect("/")
    else:
     if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
         login(request,user)
         messages.success(request,"logged in successfully")
         return redirect("/")
      else:
         messages.error(request,"Invalid User Name or Password")         
         return redirect("/login")       
    return render (request, "shop/login.html")


def register(request):
    form=CustomUserForm()
    if request.method=='POST':
       form=CustomUserForm(request.POST)
       if form.is_valid():
          form.save()
          messages.success(request,"Registration success you can login now...")
          return redirect('/login')
    return render(request, "shop/register.html",{'form':form})
def collections (request):
    catagory=Catagory.objects.filter(status=0)
    return render (request, "shop/collections.html",{"catagory":catagory})

def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render (request, "shop/products/index.html",{"products":products,"category_name":name})
    else:  
        messages.warning (request, "No Such Catagory Found")
        return redirect ('collections')

def product_details(request,cname,pname):
     if(Catagory.objects.filter(name=cname,status=0)):
       if(Product.objects.filter(name=pname,status=0)):
         products=Product.objects.filter(name=pname,status=0).first()
         return render(request, "shop/products/product_details.html",{"products":products})

       else:
         messages.error(request, "No Such Produtct Found")
         return redirect('collections')
     else:
        messages.error (request, "No Such Catagory Found")
        return redirect('collections')
     
def search(request):
    query = request.GET.get('query')
    if query:
        # Use Q objects to search in multiple fields
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )
    else:
        results = Product.objects.all()
    return render(request, 'search_results.html', {'results': results, 'query': query})

def autocomplete(request):
    query = request.GET.get('term', '')
    products = Product.objects.filter(name__icontains=query)[:10]  # Limit to 10 results
    results = [product.name for product in products]
    return JsonResponse(results, safe=False)
    