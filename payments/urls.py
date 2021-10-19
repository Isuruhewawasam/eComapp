
from payments.models import Customer
from django.urls import path
from .views import HomeView,addproductView,addCatergoryView,allCatergoryView,productdetailsView,addToCartView,CartView,ManageCartView,EmptyCartView,CheckoutView,placeOrderView,modelstaticView,modelstaticViewtemp,SliderImage,CustomerRegisterView,CustomerlogoutView,CustomerloginView,AdminRegisterView,AdminHome,AdminlogoutView,AdminloginView,adminProduct
urlpatterns = [
    ###### app urls #####
    path('',HomeView.as_view(),name='home'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('addproduct/',addproductView.as_view(),name='addproduct'),
    path('addcatergory/',addCatergoryView.as_view(),name='addcatergory'),
    path('allcatergory/',allCatergoryView.as_view(),name='allcatergory'),
    path('productdetails/<slug:slug>/',productdetailsView.as_view(),name='product_details'),
    path('addtocart/<int:pro_id>/',addToCartView.as_view(),name='add_to_cart'),
    path('cart/',CartView.as_view(),name='my_cart'),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),
    path('placeOrder/',placeOrderView.as_view(),name='place_order'),
    path('index/',modelstaticView.as_view(),name='index'),
    path('indextemp/',modelstaticViewtemp.as_view(),name='indextemp'),
    path('slider/',SliderImage.as_view(),name='slider'),

    ##### customer urls######
    path('custermor-register/',CustomerRegisterView.as_view(),name='custermor_register'),
    path('custermor-logout/',CustomerlogoutView.as_view(),name='custermor_logout'),
    path('custermor-login/',CustomerloginView.as_view(),name='custermor_login'),
    #path("empty-credit/", Emptycredit.as_view(), name="emptycredit"),

    ###Admin urls######
    path('admin-register/',AdminRegisterView.as_view(),name='admin_register'),
    path('admin-logout/',AdminlogoutView.as_view(),name='admin_logout'),
    path('admin-login/',AdminloginView.as_view(),name='admin_login'),
    path('admin-home',AdminHome.as_view(),name='admin_home'),
    path('admin-product',adminProduct.as_view(),name='admin_product'),
    


]
