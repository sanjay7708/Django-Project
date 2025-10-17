from django.contrib import admin
from . models import (Category,Product,Variation,ProductImage,Cart,cartItem,Address,
                      Order,OrderItem,ContactForm)
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Variation)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(cartItem)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ContactForm)