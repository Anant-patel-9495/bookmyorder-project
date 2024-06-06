from django.db import models

# Create your models here.

class user_info(models.Model):
    table_id = models.AutoField(primary_key=True)
    person_name = models.CharField(max_length=30)
    email_id = models.EmailField()
    phone_number = models.IntegerField()
    family_members = models.IntegerField()

    def __str__(self):
        return f'{self.table_id} - {self.person_name}'


class Dish(models.Model):
    dish_type_choices = [
        ('appetizer', 'Appetizer'),
        ('mainCourse', 'Main Course'),
        ('dessert', 'Dessert'),
    ]

    dish_type = models.CharField(max_length=20, choices=dish_type_choices)
    dish_name = models.CharField(max_length=100)
    dish_price = models.IntegerField()
    dish_description = models.TextField()
    dish_image = models.ImageField(upload_to='static/dish_image', null=True, blank=True)

    def __str__(self):
        return f'{self.dish_type} - {self.dish_name}'

    class Meta:
        ordering = ['dish_type']

class DishIngredients(models.Model):
    dish = models.ForeignKey(Dish, on_delete = models.CASCADE)
    ingredients = models.JSONField()

    def __str__(self):
        return f'Ingredients for {self.dish.dish_name}'

    class Meta:
        ordering = ['dish__dish_type']

class Order(models.Model):
    customer_id = models.ForeignKey(user_info, on_delete=models.CASCADE, default=None)
    items = models.JSONField()  # Assuming you store the items as JSON in the order
    total_amount = models.DecimalField(max_digits = 10000,decimal_places=0)
    order_date = models.DateTimeField(auto_now_add=True)
    is_order_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order for {self.customer_id.person_name} on {self.order_date}"