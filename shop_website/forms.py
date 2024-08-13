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


# class RegisterForm(forms.ModelForm):
#     # email=forms.EmailField(required=False)
#     confirm_password=forms.CharField(max_length=255)
#     class Meta:
#         model=User
#         fields=('username', 'password', 'email')

#     def clean_username(self):
#         username=self.cleaned_data.get('username')
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError('This username already exists')
#         return username
    
#     def clean(self):
#         password=self.cleaned_data.get('password')
#         confirm_password=self.cleaned_data.get('confirm_password')
#         if password != confirm_password :
#             raise forms.ValidationError('Passwords do not match')
#         return password

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255, label='Confirm Password')

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username already exists')
        return username

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     confirm_password = self.cleaned_data.get('confirm_password')
    #     if password != confirm_password:
    #         raise forms.ValidationError('Passwords do not match')
    #     return password

    def clean(self):
        cleaned_data = super().clean()  # Call the parent's clean method
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
    
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
    
        return cleaned_data  # Return all cleaned data


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Use set_password to hash the password
        if commit:
            user.save()
        return user





