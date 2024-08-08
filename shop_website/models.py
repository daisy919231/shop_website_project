from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe


class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Category(models.Model):
    title=models.CharField(max_length=70, unique=True)
    slug=models.SlugField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug=slugify(self.title)
        super(Category,self).save(*args, **kwargs)



    class Meta:
        verbose_name_plural='Categories'
        db_table='Category'

    def __str__(self) -> str:
        return self.title

class Product(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    
    name=models.CharField(max_length=100)
    description=models.TextField(null=True, blank=True)
    price=models.FloatField()
    category=models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    quantity=models.PositiveIntegerField(default=0)
    rating=models.PositiveIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value)
    discount=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to='products', default='sample_image.pg')

    class Meta:
        db_table='Product'


    
    def image_tag(self):
        return mark_safe('<img src="/products/%s" width="300" />' % (self.image))
    image_tag.short_description="Image"

    @property
    def discounted_price(self):
        if self.discount > 0:
            return int(self.price * (1-self.discount/100))
        return self.price

    def __str__(self):
        return self.name
    
    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return None
        
        

# User degan table ham yaratilishi kerak #

# class User(models.Model):
#     name=models.CharField(max_length=100)
#     address=models.TextField()
#     phone_number=models.TextField()


# Create your models here.
class Comment(BaseModel):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    product=models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
    comment=models.TextField()
    is_provided=models.BooleanField(default=True)
    
    class Meta:
        db_table='Comment'

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['product_id', 'user_id'], name='unique_product_user_comment')
#         ]

#     def __str__(self):
#         return f'Comment {self.comment_id} by {self.user_id} on {self.product_id}'

class Order(BaseModel):
    name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=13)
    product=models.ForeignKey('Product', on_delete=models.CASCADE, related_name='orders')
    order_quantity=models.PositiveIntegerField(default=0)

    def __str__(self):
        return (self.name + '' + self.phone_number)
    class Meta:
        db_table='Order'

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['user_id'], name='unique_user_order')
#         ]




    