from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(user_info)
admin.site.register(Dish)
admin.site.register(DishIngredients)
admin.site.register(Order)