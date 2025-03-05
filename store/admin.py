from django.contrib import admin
from .models import CarouselImage
from .models import Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_30ml', 'price_50ml', 'created_at')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return obj.image1 and f'<img src="{obj.image1.url}" width="50" height="50"/>'

    image_preview.allow_tags = True
    admin.site.register(CarouselImage)

    
    