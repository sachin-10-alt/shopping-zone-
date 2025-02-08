from django.contrib import admin
from .models import *
"""
class categoryAdmin(admin.ModelAdmin):
    list_display = ('name','image','description')
admin.site.register(Catagory,categoryAdmin)
"""
admin.site.register(Catagory)
admin.site.register(Product)
