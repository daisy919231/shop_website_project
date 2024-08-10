from django import forms 
from shop_website.models import Comment,Order, Product
from django.contrib.auth.models import User

class CommentModelForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields='__all__'
        # fields=['name, 'email, 'comment']
        exclude = ( 'product',)

    def clean_email(self):
        email=self.data.get('email')
        if Comment.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This {email} was already used! ')
        return email


class OrderModelForm(forms.ModelForm):
    class Meta:
        model=Order
        exclude = ( 'product',)



class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields='__all__'




class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

    def clean_username(self):
        username=self.data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'The user has not been found')
        return username






