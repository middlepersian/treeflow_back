from django.contrib import admin

# Register your models here.


from .models import Image, ImageSection

admin.site.register(Image)
admin.site.register(ImageSection)