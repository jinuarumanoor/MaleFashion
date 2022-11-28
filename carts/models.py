from django.db import models
from store.models import Product, Variation
from accounts.models import Account



# Create your models here.
class Cart(models.Model):
    cart_id =models.CharField(max_length=250,blank=True)
    data_added =models.DateField(auto_now_add=True)


    def __str__(self):
        return self.cart_id

class wishlist(models.Model):
    Product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

class CartItem(models.Model):
    user= models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)   
    variations  = models.ManyToManyField(Variation, blank=True)    
    cart    = models.ForeignKey(Cart,on_delete=models.CASCADE, null=True)    
    quantity =models.IntegerField()
    is_active = models.BooleanField(default=True) 

    def sub_total(self):
        if self.product.offer_price == 0:
            return self.product.price * self.quantity
        else:
            return self.product.offer_price * self.quantity
    def __unicode__(self):
        return self.product
    


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10, blank=True)
    discount = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.coupon_code


class UsedCoupon(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True)    