from multiprocessing import context
from django.shortcuts import render
from store.models import Product

def home(request):
    products= Product.objects.all().filter(is_available=True)

    for product in products:
        if product.Offer_Price():
                new=Product.Offer_Price(product)
                product.offer_price=new["new_price"]
                product.percentage=new["discount"]
                product.save()
        else:
                product.offer_price=0
                product.save()

    context ={
            'products': products,
    }
    return render(request,'home.html',context)