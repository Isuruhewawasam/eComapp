
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField
from django.urls import reverse

# Create your models here.

class Admin_user(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    joined_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user)


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200 ,null= True, blank=True )
    joined_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user)


# CATERGORY STORE KARANA DATABASE EKA
class Catergory(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("admin_product")


# PRODUCT STORE KARANA DATABASE EKA
class Product(models.Model):
    catergory = models.ForeignKey(Catergory,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=500)
    slug = models.SlugField(unique=True)
    image =models.ImageField(upload_to= 'products')
    market_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    discriptions = models.TextField()
    worenty = models.CharField(max_length=200,null=True,blank=True)
    return_policy =models.CharField(max_length=200,null=True,blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product_name

class Pimage(models.Model):
    proimage=models.ForeignKey(Product,on_delete=models.CASCADE)
    ima =models.ImageField(upload_to='product/images')

    def __str__(self):
        return self.proimage
    
    

#ALUTHIN CART EKAK CREATE KALAMA EKA STORE WENA DATABASE EKA
class Cart(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    total = models.PositiveIntegerField(default=0)
    creat_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Cart:' + str(self.id)


#CART EKATA PRODUCT ADD KALAMA EKE DATA STORE WENA DARTABASE EKA
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return 'Cart:' + str(self.cart.id) + 'Cart product:' + str(self.id)


# ORDER EKA GATHTHAMA STORE KARANA DETABASE EKA
Order_Status={
    ('order received','order received '),
    ('order processing','order processing '),
    ('order is on the way','order is on the way '),
    ('order completed','order completed '),
    ('order cancled','order canceled '),

}
payment_choice={
    ('Cash on Delivery','Cash on Delivery '),
    ('Card Payment','Card Payment '),

}
class Order(models.Model):
    cart = OneToOneField(Cart,on_delete=models.CASCADE)
    order_by = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    town = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=200,choices=Order_Status)
    created_at = models.DateTimeField(auto_now_add=True)
    pyment_method = models.CharField(max_length=30,choices=payment_choice,default='Cash on Delivery')

    def __str__(self):
        return 'Order:'+ str(self.id) 
    
class slider(models.Model):
    image =models.ImageField(upload_to= 'products')

    

    def get_absolute_url(self):
        return reverse("slider")
    
    
    