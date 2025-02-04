from django.contrib import admin
from django.urls import path
from shop_website.views import views, auth
urlpatterns=[
    path('admin/',admin.site.urls),
    path('product-list/', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='category_detail_id'),
    path('pd/<int:product_id>', views.product_details, name='product_details'),
    path('product/<int:product_id>/add-comment/', views.add_comment, name='add_comment'),
    path('product/<int:product_id>/place-order/', views.place_order, name='place_order'),
    path('add-product/', views.add_product, name='add_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('login-page/', auth.login_page, name='login_page'),
    path('register-page/', auth.register_page, name='register_page'),
    path('logout-page/', auth.logout_page, name='logout_page'),


    


]