from django.db import models
from category.models import Category
from django.urls import reverse
from brand.models import Brand
from django.utils import timezone
from django.apps import apps
from django.db.models import Sum




# Create your models here.

class Product(models.Model):
    product_name        = models.CharField(max_length=200,unique=True)
    slug                = models.SlugField(max_length=200,unique=True)
    description         = models.TextField(max_length=500,blank=True)
    price               = models.IntegerField()
    offer_price = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    images              = models.ImageField(upload_to='photos/products')
    stock               = models.IntegerField()
    is_available        = models.BooleanField(default=True)
    category            = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)
   
  
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
    def __str__(self):
        return self.product_name

    def Offer_Price(self):
        try:
            if self.productoffer.is_valid:
                offer_price = (self.price * self.productoffer.discount) / 100
                new_price = self.price - offer_price
                return {
                    "new_price": new_price,
                    "discount": self.productoffer.discount,
                }
            raise
       
        except:
                try:
                    if self.category.categoryoffer.is_valid:
                        offer_price = (
                                              self.price * self.category.categoryoffer.discount
                                      ) / 100
                        new_price = self.price - offer_price
                        return {
                            "new_price": new_price,
                            "discount": self.category.categoryoffer.discount,
                        }
                    raise
                except:
                    pass        
    def get_count(self, month=timezone.now().month):
        orderproduct = apps.get_model("orders", "OrderProduct")
        order = orderproduct.objects.filter(
            product=self, created_at__month=month)
        return order.values("product").annotate(quantity=Sum("quantity"))

    def get_revenue(self, month=timezone.now().month):
        orderproduct = apps.get_model("orders", "OrderProduct")
        orders = orderproduct.objects.filter(
            product=self, created_at__month=month
        )
        return orders.values("product").annotate(revenue=Sum("product_price"))

    def get_profit(self, month=timezone.now().month):
        orderproduct = apps.get_model("orders", "OrderProduct")
        orders = orderproduct.objects.filter(
            product=self, created_at__month=month
        )
        profit_calculted = orders.values("product").annotate(
            profit=Sum("product_price")
        )
        profit_calculated = profit_calculted[0]["profit"] * 0.23
        return profit_calculated


class VariationManager(models.Manager):
  
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)


variation_category_choice = (

    ('size','size'),
)

class Variation(models.Model):
    product           = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=variation_category_choice)
    variation_value    = models.CharField(max_length=100)
    is_active         = models.BooleanField(default=True)
    created_date      = models.DateTimeField(auto_now=True)


    objects = VariationManager()


    def __str__(self):
        return self.variation_value

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'        
    





