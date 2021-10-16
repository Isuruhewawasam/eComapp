from django import forms
from .models import Product,Catergory,Order,slider,Customer,Admin_user
from django.contrib.auth.models import User



class productForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

       
        widgets ={

            'catergory':forms.Select(attrs={'class':'form-control'}),
            'product_name':forms.TextInput(attrs={'class':'form-control'}),
            'slug':forms.TextInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'market_price':forms.TextInput(attrs={'class':'form-control'}),
            'selling_price':forms.TextInput(attrs={'class':'form-control'}),
            'discriptions':forms.Textarea(attrs={'class':'form-control'}),
            'worenty':forms.TextInput(attrs={'class':'form-control'}),
            'return_policy':forms.TextInput(attrs={'class':'form-control'}),
            'view_count':forms.TextInput(attrs={'class':'form-control'}),
            
        }

class CatergoryForm(forms.ModelForm):
    class Meta:
        model = Catergory
        fields = '__all__'

        widgets ={

            'title':forms.TextInput(attrs={'class':'form-control'}),
            'slug':forms.TextInput(attrs={'class':'form-control'}),
            

        }

class placeOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_by','last_name','shipping_address','town','mobile','email','pyment_method']

        widgets={
            'order_by':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'shipping_address':forms.TextInput(attrs={'class':'form-control'}),
            'town':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'pyment_method':forms.Select(attrs={'class':'form-control'}),


        } 

class sliderImageform(forms.ModelForm):
    class Meta:
        model = slider
        fields = '__all__'

        widgets={
            'image':forms.FileInput(attrs={'class':'form-control'}),
        }
class Adminform(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Admin_user
        fields = ["username","password","email","full_name"]

        widgets={
            'full_name':forms.TextInput(attrs={'class':'form-control'}),
            
        }
## user kalin register welada kiyala validate karana vidiya
    def clean_username(self):
        uname = self.cleaned_data.get('username')
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError('user already exists')
        return uname

class customerform(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Customer
        fields = ["username","password","email","full_name","address"]

        widgets={
            'full_name':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
        }
## user kalin register welada kiyala validate karana vidiya
    def clean_username(self):
        uname = self.cleaned_data.get('username')
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError('user already exists')
        return uname

class loginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

