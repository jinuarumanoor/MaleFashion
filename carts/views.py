from django.shortcuts import render,redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart,CartItem,Coupon, UsedCoupon
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import wishlist
from django.http import JsonResponse
from django.contrib import messages
from store.models import Product






# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart    

def add_cart(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)  # To get the product
    #if the user is aunthenticated
    
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    # If the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
def remove_cart(request,product_id,cart_item_id):
  
    product = get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product ,user=request.user,id=cart_item_id)
        else:
            cart= Cart.objects.get(cart_id =_cart_id(request))
            cart_item = CartItem.objects.get(product=product ,cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:
           cart_item.quantity -= 1
           cart_item.save()
        else:
           cart_item.delete()
    except:
        pass 
    return redirect('cart')    

def remove_cart_item(request,product_id,cart_item_id):
   
    product = get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product ,user=request.user,id=cart_item_id)
    else:
         cart= Cart.objects.get(cart_id =_cart_id(request))
         cart_item = CartItem.objects.get(product=product ,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request,total =0,quantity=0,cart_items=None, reduction=0):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
             cart_items = CartItem.objects.filter(user=request.user,is_active=True)
             if 'coupon_code' in request.session:
                coupon = Coupon.objects.get(coupon_code=request.session['coupon_code'])
                reduction = coupon.discount
             else:
                reduction = 0
        else:
             cart=Cart.objects.get(cart_id=_cart_id(request))
             cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            if cart_item.product.offer_price == 0:
             total +=(cart_item.product.price * cart_item.quantity)

            else:
             total += (cart_item.product.offer_price * cart_item.quantity)
             quantity+= cart_item.quantity
        tax= (2*total)/100    
        grand_total=total + tax - reduction
    except ObjectDoesNotExist:
        pass # just ignore

    context ={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax'       :tax,
        'grand_total':grand_total,
    }

    return render(request,'store/cart.html',context)


@login_required(login_url='user_login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:

        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            if cart_item.product.offer_price== 0:
                total += (cart_item.product.price * cart_item.quantity)
            else:    
           
                total += (cart_item.product.offer_price * cart_item.quantity)

                quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax 
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/checkout.html', context)
def wish_list(request):
    flag=0
    id= request.GET["id"]
    product=Product.objects.get(id=id)
    if wishlist.objects.filter(Product=product, user=request.user).exists():
        flag=1
    else:
        wishlist.objects.create(Product=product,user=request.user)
        flag=2

    context={
        "flag":flag
    }
    return JsonResponse(context)

def viewwish_list(request):
    Wishlist = wishlist.objects.filter(user=request.user)
    context={
        'wishlist':Wishlist
    }
    return render(request, 'store/wish_list.html',context)    

def coupon_apply(request):
    if request.method == 'POST':
        print('coupon')
        coupon_code = request.POST.get('coupon_code')
        print(coupon_code)
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            if coupon is not None:
                try:
                    UsedCoupon.objects.get(coupon = coupon, user = request.user)
                    print('coupon already used')
                   
                except:
                    request.session['coupon_code'] = coupon_code
                    
                
        except:
            messages.info(request, "Invalid Coupon")
    return redirect(cart)    
