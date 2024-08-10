from django.contrib import admin
from .models import Category, Product, Comment, Order
from django.contrib.auth.models import User, Group
from shop_website.simple_admin_filter import IsExpensiveFilter, IsLotFilter


# Register your models here.
# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(User)
# admin.site.register(Comment)
# admin.site.register(Order)

# admin.site.register(User)
admin.site.unregister(Group)






@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display=('title', 'slug', 'product_count')
    search_fields=['title', 'id']
    prepopulated_fields={'slug':('title',)}


    def product_count(self, obj):
        return obj.products.count()


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=('name', 'slug', 'price', 'comment_count', 'order_count', 'category', 'is_expensive',) #'image_tag',)
    list_filter=('discount', IsExpensiveFilter)
    search_fields=['name', 'price']
    # fields=['image_tag']
    # readonly_fields=['image_tag']
    
    def is_expensive(self,obj):
        return obj.price > 500
    
    is_expensive.boolean=True


    def comment_count(self, obj):
        return obj.comments.count()

    def order_count(self, obj):
        return obj.orders.count()


    

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'product')
    search_fields=['title', 'email']

    

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display=('id', 'name')
    search_fields=['title', 'phone_number']
    list_filter=['product', IsLotFilter]

    def is_lot(self,obj):
        return obj.price > 5
    
    is_lot.boolean=True


    