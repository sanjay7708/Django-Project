from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=100,unique=True,blank=True)
    parent=models.ForeignKey("self",on_delete=models.CASCADE,null=True,blank=True,related_name='children')

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args,**kwargs)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural='Categories'
class Product(models.Model):
    short_name=models.CharField(max_length=100)
    full_name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products",null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.short_name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.short_name
class Variation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="variations")
    variation_type=models.CharField(max_length=100)
    value=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)


    def __str__(self):
        return f"{self.product.short_name}-{self.variation_type}:{self.value}"
    
class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    image=models.ImageField(upload_to="products/")
    

    def __str__(self):
        return f"Image for {self.product.short_name}"
class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Cart of {self.user.username}"
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
class cartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="cart_items")
    variation=models.ForeignKey(Variation,on_delete=models.CASCADE,blank=True,null=True)
    quantity=models.PositiveIntegerField(default=1)


    class Meta:
        unique_together=("cart","product","variation")
    def __str__(self):
        return f"{self.product.short_name} ({self.variation})x {self.quantity}"
    @property
    def subtotal(self):
        price=self.variation.price if self.variation and self.variation.price else self.product.base_price
        return price*self.quantity

class Address(models.Model):
    ADDRESS_CHOICES=(
        ("HOME","Home"),
        ("OFFICE","Office")
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="address")
    address_type=models.CharField(max_length=50,choices=ADDRESS_CHOICES,default="Home")
    building_no=models.CharField(max_length=50)
    street_name=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100,default='India')
    country_code=models.CharField(max_length=5,blank=True,null=True,default='+91')
    pincode=models.CharField(max_length=50)
    phoneNumber=models.CharField(max_length=10,blank=True,null=True)
    is_default=models.BooleanField(default=False,blank=True,null=True)
    def __str__(self):
        return f"{self.user.username}'s {self.address_type.title()} address"
    def save(self,*args,**kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user,is_default=True).update(is_default=False)
        super().save(*args,**kwargs)
        

class Order(models.Model):
   
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,blank=True)
    total_price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"order #{self.id} by {self.user.username}"
    
    def calculated_total(self):
        total = sum(item.subtotal() for item in self.items.all())
        print('this is total:',total)
        self.total_price = total
        self.save(update_fields=["total_price"])
        return total
    
class OrderItem(models.Model):
    STATUS_CHOICES=(
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    )
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    variation=models.ForeignKey(Variation,on_delete=models.SET_NULL,blank=True,null=True)
    status=models.CharField(max_length=100,choices=STATUS_CHOICES,default='PENDING')
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)


    def __str__(self):
        if self.variation:
            return f"{self.product.short_name}x{self.variation}"
        return f"{self.product.short_name}"
        
    def subtotal(self):
        if not self.price:
            return 0
        return self.price*self.quantity
    def save(self, *args, **kwargs):
        
        if self.variation and self.variation.price:
            self.price = self.variation.price
        elif self.product:
            self.price = self.product.base_price
        super().save(*args, **kwargs)
        if self.order_id:
            self.order.calculated_total()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)

        # ✅ recalc order after delete
        if order:
            order.calculated_total()
    


class ContactForm(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    message=models.TextField()

    def __str__(self):
        return f"{self.name}'s messages"