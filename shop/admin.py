from django.contrib import admin
from .models import Catagory, Product
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
admin.site.register(User, UserAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description')

admin.site.register(Catagory, CategoryAdmin)
admin.site.register(Product)
