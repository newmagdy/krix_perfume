from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image1 = models.ImageField(upload_to='products/')
    price_30ml = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    price_50ml = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    desc1 = models.CharField(max_length=255, blank=True, null=True)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    desc2 = models.CharField(max_length=255, blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    desc3 = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel_images/')
    caption = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return f"Carousel Image {self.id}"

class Order(models.Model):
    SHIPPING_CHOICES = [
        ('standard', 'Standard Shipping'),
        ('express', 'Express Shipping'),
    ]
    PAYMENT_CHOICES = [
        ('cash_on_delivery', 'Cash on Delivery'),
        ('instapay', 'Instapay'),
    ]

    CITY_CHOICES = [
        ("new cairo", "New cairo"),
        ("nasr city", "nasr city"),
        ("masr el gdida", "masr el gdida"),
        ("madinty", "madinty"),
        ("zamalek", "zamalek"),
        ("dokki", "dokki"),
        ("mohndsen", "mohndsen"),
        ("sheikh zayed", "sheikh zayed"),
    ]

    order_id = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    additional_info = models.TextField(blank=True, null=True)
    shipping_method = models.CharField(max_length=50)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity}x {self.product_name}({self.size}) - Order {self.order.order_id}"