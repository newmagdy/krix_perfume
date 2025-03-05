import email
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.crypto import get_random_string
from django import forms
from .models import Product, CarouselImage, Order, OrderItem
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings




def home(request):
    carousel_images = CarouselImage.objects.all()  
    return render(request, 'store/home.html', {'carousel_images': carousel_images})


def products_view(request):
    products = Product.objects.all()
    return render(request, "store/products.html", {"products": products})


def product_details(request, product_key):
    product = get_object_or_404(Product, id=product_key)
    return render(request, 'store/product_details.html', {'product': product})

def add_to_cart(request, product_key):
    product = get_object_or_404(Product, id=product_key)
    cart = request.session.get('cart', {})

    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size', '30ml')

    key = f"{product_key}_{size}"  

    if key in cart:
        cart[key]['quantity'] += quantity
    else:
        price = product.price_30ml if size == '30ml' else product.price_50ml
        cart[key] = {
            'name': product.name,
            'price': float(price),
            'quantity': quantity,
            'size': size,
            'image': product.image1.url,
        }

    request.session['cart'] = cart
    request.session['cart_count'] = sum(item['quantity'] for item in cart.values())

    messages.success(request, 'Product added to cart successfully!')
    return redirect(request.META.get('HTTP_REFERER', 'home'))




# View Cart
def cart_view(request):
    cart = request.session.get('cart', {})
    for key, item in cart.items():
        item['total_price'] = item['price'] * item['quantity']  
    total_price = sum(item['total_price'] for item in cart.values())  
    return render(request, 'store/cart.html', {'cart': cart, 'total_price': total_price})

def update_cart(request, product_key, action):
    cart = request.session.get('cart', {})
    
    if product_key in cart:
        if action == "increase":
            cart[product_key]['quantity'] += 1
        elif action == "decrease":
            if cart[product_key]['quantity'] > 1:
                cart[product_key]['quantity'] -= 1
            else:
                del cart[product_key] 
    
    request.session['cart'] = cart
    request.session['cart_count'] = sum(item['quantity'] for item in cart.values())
    return redirect('cart_view')


def clear_cart(request):
        request.session['cart'] = {}
        request.session['cart_count'] = 0
        return redirect('cart_view')


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city_choices = [
        ("new cairo", "New cairo"),
        ("nasr city", "nasr city"),
        ("masr el gdida", "masr el gdida"),
        ("madinty", "madinty"),
        ("zamalek", "zamalek"),
        ("dokki", "dokki"),
        ("mohndsen", "mohndsen"),
        ("sheikh zayed", "sheikh zayed"),
    ]
    city = forms.ChoiceField(choices=city_choices, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    additional_info = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    shipping_method = forms.ChoiceField(choices=[
        ("Standard", "Standard Shipping (60 EGP)"),
        ("Express", "Express Shipping (100 EGP)"),
    ], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    payment_method = forms.ChoiceField(choices=[
        ("Cash on Delivery", "Cash on Delivery"),
        ("Instapay", "Instapay"),
    ], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
# Checkout View
def checkout_view(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('cart_view')

    total_price = sum(float(item['price']) * int(item['quantity']) for item in cart.values())

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                shipping_method = form.cleaned_data["shipping_method"]
                if shipping_method == "Standard":
                    shipping_cost = 60
                elif shipping_method == "Express":
                    shipping_cost = 100
                else:
                    shipping_cost = 0

                total_price_with_shipping = total_price + shipping_cost

                # Create Order
                order = Order.objects.create(
                    order_id=get_random_string(10).upper(),
                    full_name=form.cleaned_data["full_name"],
                    email=form.cleaned_data["email"],
                    phone_number=form.cleaned_data["phone_number"],
                    city=form.cleaned_data["city"],
                    additional_info=form.cleaned_data["additional_info"],
                    shipping_method=shipping_method,
                    payment_method=form.cleaned_data["payment_method"],
                    shipping_cost=shipping_cost,
                    total_price=total_price_with_shipping,
                )

                for key, item in cart.items():
                    OrderItem.objects.create(
                        order=order,
                        product_name=item["name"],
                        quantity=item["quantity"],
                        price=item["price"],
                        size=item["size"],
                    )

                request.session["cart"] = {}
                request.session["cart_count"] = 0

                customer_subject = "Order Confirmation - Krix Perfumes"
                customer_message_html = render_to_string('store/emails/order_confirmation_customer.html', {
                    'order': order,
                    'cart': cart,
                })
                customer_message_plain = strip_tags(customer_message_html)

                send_mail(
                    customer_subject,
                    customer_message_plain,
                    settings.DEFAULT_FROM_EMAIL,
                    [form.cleaned_data["email"]],
                    html_message=customer_message_html
                )

                owner_subject = "New Order Received - Krix Perfumes"
                owner_message_html = render_to_string('store/emails/order_notification_owner.html', {
                    'order': order,
                    'cart': cart,
                })
                owner_message_plain = strip_tags(owner_message_html)

                send_mail(
                    owner_subject,
                    owner_message_plain,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    html_message=owner_message_html
                )

                messages.success(request, "Your order has been placed successfully!")
                return redirect("home")

            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect("home")

        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = CheckoutForm()

    return render(request, "store/checkout.html", {
        "form": form,
        "cart": cart,
        "total_price": total_price
    })

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        comments = request.POST.get('comments')

        subject = f'New Contact Form Submission from {name}'
        message = f'Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{comments}'

        send_mail(
            subject,
            message,
            'krixperfume@gmail.com',  # Your email
            ['krixperfume@gmail.com'],  # Send to yourself (or a support email)
            fail_silently=False,
        )

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('store/contact')

    return render(request, 'store/contact.html')

def adminorders_password_protect(request):
    request.session.pop('adminorders_authenticated', None)  # Clear session every time you visit password page (optional)
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == 'K@12345678':  # Replace with your actual password
            request.session['adminorders_authenticated'] = True
            return redirect('adminorders')
        else:
            error = "Invalid password. Please try again."
            return render(request, 'store/password_protect.html', {'error': error})

    return render(request, 'store/password_protect.html')

# This is the actual orders page (only visible if authenticated)
def adminorders_views(request):
    if not request.session.get('adminorders_authenticated'):
        return redirect('adminorders_protect')

    if request.GET.get('logout'):
        request.session.pop('adminorders_authenticated', None)
        return redirect('adminorders_protect')

    orders = Order.objects.filter(payment_method__isnull=False).order_by('-created_at')
    return render(request, 'store/adminorders.html', {'orders': orders})