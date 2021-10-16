
from django import forms
from django.contrib.auth.models import User
from django.db.models.query import InstanceCheckMeta
from django.http import request
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,FormView,View
from.forms import productForm,CatergoryForm,placeOrder,sliderImageform,customerform,loginForm,Adminform
from.models import Cart, CartProduct, Order, Product,Catergory,slider,Customer,Admin_user
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy,reverse
from django.core.paginator import Paginator



# Create your views here.



class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart_obj= Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()

        return super().dispatch(request, *args, **kwargs)
    



# CHECKOUT KARANA VIEW EKA
class CheckoutView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        order = Order.objects.get(id=o_id)
        context = {
            "order": order
            
        }
        return render(request, "checkout.html", context)


#HOME VIEW EKA
class HomeView(EcomMixin, TemplateView):
    template_name ='home.html'
    def get_context_data(self, **kwargs):
        contex=super().get_context_data(**kwargs)
        product_obj = Product.objects.all().order_by('-id')
        ## paginator eka hadana vidiya
        paginator = Paginator(product_obj, 3) # Show 3 contacts per page.
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        
        contex['product']=product_list
        ## slider eka
        contex['product_slider']=slider.objects.all().order_by('-id')[:5]
        ## new items slide eka
        contex['new_items']= Product.objects.all().order_by('-id')[:6]
        return contex


# PRODUCT ADD KARANA VIEW EKA
class addproductView(CreateView):
    model = Product
    form_class = productForm
    template_name ='addproduct.html'


# CATERGORY ADD KARANA VIEW EKA
class addCatergoryView(CreateView):
    model = Catergory
    form_class = CatergoryForm
    template_name ='addcatergory.html'


# CATERGORY WIDIYATA PRODUCT PENNANA VIEW EKA
class allCatergoryView(EcomMixin,TemplateView):
    template_name = 'allcatergory.html'
    def get_context_data(self, **kwargs):
        contex =super().get_context_data(**kwargs)
        contex['allcatergory']= Catergory.objects.all()
        return contex


# PRODUCT DETAILS PENNANA VIEW EKA
class productdetailsView(EcomMixin,TemplateView):
    template_name= 'details.html'
    def get_context_data(self, **kwargs): 
        contex = super().get_context_data(**kwargs)
        url_slug =self.kwargs['slug']
        product=Product.objects.get(slug=url_slug)
        product.view_count +=1
        product.save()
        contex['product_details']=product
        return contex


# CART EKATA PRODUCT ADD KARANA SAHA CART EKA CREATE KARANA VIEW EKA
class addToCartView(EcomMixin,TemplateView):
    template_name='add_to_cart.html'

                     
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        return context



# CART EKA PENNANA VIEW EKA
class CartView(EcomMixin, TemplateView):
    template_name = 'cart.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


# CART EKE PRODUCT ADU WADI SAHA REMUVE KARANA VIEW EKA
class ManageCartView(EcomMixin,View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("/cart/")


# CART EKA SAMPUURNAYENMA EMTEY KARANA VIEW EKA
class EmptyCartView(EcomMixin,View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("/cart/")


# ORDER EKA PLEACE KARANA SAHA ORDER EKE FORM EKA PURAWANA VIEW EKA
class placeOrderView(CreateView):
    template_name = 'placeorder.html'
    form_class = placeOrder
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.customer:
            pass
        else:
            return redirect("/custermor-login/?next=/placeOrder/")  ###?next=/checkout/

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


# ORDER PLEACING FORM EKA
    def form_valid(self, form):
        cart_id =self.request.session.get('cart_id')
        if cart_id:
            cart_obj= Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "order received"
            pm = form.cleaned_data.get('pyment_method')
            order=form.save()
            # SESSON EKE HADAPU CART_ID EKA ORDER EKA PLACE KALATA PASSE DELETE KIREEMA
            del self.request.session['cart_id']
            # payment options therima
            if pm =='Card Payment':
                return redirect(reverse_lazy('checkout')+ "?o_id=" + str(order.id))

                
        else:
            return redirect('/home/')
        return super().form_valid(form)



class modelstaticView(TemplateView):
    template_name='index.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['my name']=Product.objects.all()
        
        return context

class modelstaticViewtemp(TemplateView):
    template_name='indextem.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['product']=Product.objects.all()
        return context


## slider add karana view eka
class SliderImage(CreateView):
    model = slider
    form_class = sliderImageform
    template_name ='slider.html'


### admin home eka
class AdminHome(TemplateView):
    template_name='admin_register/admin_home.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['order']=Order.objects.all()
        return context

## Admin add karana view eka
class AdminRegisterView(CreateView):
    form_class = Adminform
    template_name ='admin_register/admin_register.html'
    success_url= reverse_lazy('admin_home')
## Admin form eken auth User ekata onetoone field walin add karana method eka
    def form_valid(self, form):
        
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = User.objects.create_user(username,email,password)
        form.instance.user= user
        login(self.request,user)
        return super().form_valid(form)

class AdminlogoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse_lazy('admin_home'))

class AdminloginView(FormView):

    success_url= reverse_lazy("admin_home")
    form_class = loginForm
    template_name ='admin_register/admin_login.html'
    
## form eken authenticate karala user innawada balana method eka
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname,password=pword)
        if usr is not None and Admin_user.objects.filter(user = usr).exists():
            login(self.request, usr)
        else:
            return render(self.request,self.template_name, {"form" : self.form_class,'error':'user is invalid'})

        return super().form_invalid(form)


## customer add karana view eka
class CustomerRegisterView(CreateView):
    form_class = customerform
    template_name ='customer_register.html'
    success_url= reverse_lazy('home')
## custermor form eken auth User ekata onetoone field walin add karana method eka
    def form_valid(self, form):
        
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = User.objects.create_user(username,email,password)
        form.instance.user= user
        login(self.request,user)
        return super().form_valid(form)

class CustomerlogoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse_lazy('home'))

class CustomerloginView(FormView):

    success_url= reverse_lazy("home")
    form_class = loginForm
    template_name ='customer_login.html'
    
## form eken authenticate karala user innawada balana method eka
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname,password=pword)
        if usr is not None and Customer.objects.filter(user = usr).exists():
            login(self.request, usr)
        else:
            return render(self.request,self.template_name, {"form" : self.form_class,'error':'user is invalid'})

        return super().form_invalid(form)
        
##  success_url eka override karana vidiya
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url
            



