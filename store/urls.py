
from django.urls import path
from .views import home, products_view, product_details, add_to_cart, cart_view,update_cart,clear_cart,contact_view,adminorders_views,adminorders_password_protect
from django.conf import settings
from django.conf.urls.static import static
from .views import checkout_view



urlpatterns = [
    path('', home, name='home'),  
    path('products/', products_view, name='products'),
    path('product/<int:product_key>/', product_details, name='product_details'),
    path('add-to-cart/<int:product_key>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('update-cart/<str:product_key>/<str:action>/', update_cart, name='update_cart'),
    path('checkout/', checkout_view, name='check_out'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('contact/', contact_view, name='contact'),
    path('adminorders/', adminorders_views, name='adminorders'),
    path('adminorders-protect/', adminorders_password_protect, name='adminorders_protect'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
