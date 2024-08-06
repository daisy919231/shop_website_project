from django.shortcuts import render, HttpResponse, get_object_or_404,redirect
from shop_website.models import Category, Product, Comment, Order
from typing import Optional
from shop_website.forms import CommentModelForm, OrderModelForm, ProductModelForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.
def product_list(request, category_id: Optional[int]=None ):
    categories=Category.objects.all().order_by('id')
    search=request.GET.get('q')
    filter_type=request.GET.get('filter', '')
    if category_id:
        if filter_type == 'expensive':
            products=Product.objects.filter(category=category_id).order_by('-price')
        elif filter_type=='cheap':
            products=Product.objects.filter(category=category_id).order_by('price')
        elif filter_type == 'quality_products':
             products=Product.objects.filter(Q(category=category_id) & Q(rating__gte=4)).order_by('-rating')
        else:
            products=Product.objects.filter(category=category_id)
            
    else:
        if filter_type == 'expensive':
            products=Product.objects.all().order_by('-price')
        elif filter_type=='cheap':
            products=Product.objects.all().order_by('price')
        elif filter_type == 'quality_products':
             products=Product.objects.filter(Q(rating__gte=4)).order_by('-rating')
        else:
            products = Product.objects.all()
    if search:
        products=products.filter(Q(name__icontains=search)| Q(comments__comment__icontains=search)).distinct()
    context={
    'products': products,
    'categories': categories } 
    return render (request, 'shop_website/home.html', context)

def product_details (request, product_id, category_id, displayed_product_id):
    search=request.GET.get('q')
    categories=Category.objects.all()
    product=Product.objects.get(id=product_id)
    comments=Comment.objects.filter(product=product_id, is_provided=True).order_by('-id')
    if search:
        comments=comments.filter(Q(comment__icontains=search))
        # if not related to only one product, but for all products:
        # comments=Comment.objects.filter(Q(comment__icontains=search))
    context={
        'product': product,
        'comments': comments,
        'categories': categories, 
        'comments': comments
        }
    return render (request, 'shop_website/detail.html', context)


# def add_comment(request, product_id):
    product=get_object_or_404(Product, id=product_id)
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        comment=request.POST.get('comment')
        user_comment=Comment(name=name, email=email, comment=comment)
        user_comment.product=product
        user_comment.save()
        return redirect ('product_details', product_id)
    else:
        pass
    return render(request, 'shop_website/detail.html')

def add_comment(request, product_id):
    product=get_object_or_404(Product, id=product_id)
    if request.method=='POST':
        form=CommentModelForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.product=product
            comment.save()
            return redirect('product_details', product_id)
    else:
        form=CommentModelForm()
    context={
        'form':form,
        'product': product
    }

    return render(request, 'shop_website/detail.html', context )


# PLACE ORDER HttpResponseRedireect bilan

def place_order(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        form = OrderModelForm(request.POST or None)
        order_quantity = int(request.POST.get('order_quantity', 0))

        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            
            
            if order_quantity > 0 and order_quantity <= product.quantity:
                order = Order.objects.create(
                name=request.POST.get('name'),
                phone_number=request.POST.get('phone_number'),
                product=product,
                order_quantity=order_quantity
                    )
                product.quantity -= order_quantity
                order.save()
                messages.success(request, 'Your order has been secured!')
                product.save()
                positive_message= HttpResponseRedirect('/success/')
                print(positive_message)
                return redirect('product_list')
               
    
            else:
                messages.error(request, 'Your order does not fit the storage capability')
                negative_message=HttpResponseRedirect('/error')
                print(negative_message)
                form=CommentModelForm()

    context = {
        'form': form,
        'product': product
            }
    return render(request, 'shop_website/detail.html', context)





# PLACE ORDER messages.add_message bilan

# def place_order(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     form=OrderModelForm()

#     if request.method=='POST':
#         form=OrderModelForm(request.POST)
#         if form.is_valid():
#             order=form.save(commit=False)
#             order.product=product
#             if product.quantity >= order.order_quantity:
#                 product.quantity -= order.order_quantity
#                 order.save()
#                 product.save()
#                 messages.add_message(
#                     request, 
#                     level=messages.SUCCESS,
#                     message='Your order has been sucessfully saved!'
#                 )
#                 return redirect('product_details', product_id)
#             else:
#                 messages.add_message(
#                     request, 
#                     level=messages.ERROR,
#                     message = 'Insufficient storage'
#                 )
        
#     context= {
#         'form': form,
#         'product': product
#         }
        
#     return render(request, 'shop_website/detail.html',context)

@login_required
def add_product(request):
    form=ProductModelForm()
    if request.method=='POST':
        form=ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    
    context={
        'form':form
    }

    return render (request, 'shop_website/add_product.html', context)


@login_required
def delete_product(request, product_id):
    product=get_object_or_404(Product, id=product_id)
    if product:
        product.delete()
        return redirect('product_list')
        
@login_required
def edit_product(request, product_id):
    product=get_object_or_404(Product, id=product_id)
    form=ProductModelForm(instance=product)
    if request.method=='POST':
        form=ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_details', product_id)
        
    context={
            'form':form
            }

    return render (request, 'shop_website/edit-product.html', context)

def related_products(request, category_id, displayed_product_id):
    category=get_object_or_404(Category, id=category_id)
    products=Product.objects(category=category).exclude(id=displayed_product_id)
    context={
        'category':category,
        'products':products,
    }
    return render (request, 'shop_website/detail.html', context)


