from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from OnlineRestaurant.mainpage import *
from OnlineRestaurant.hotelmenu import *
import random
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http import JsonResponse
import json

# Create your views here.
def basepage(request):
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        family_members = request.POST.get('family_members')

        user_instance = user_info(person_name= name, email_id= email, phone_number= phone, family_members= family_members)
        user_instance.save()

        return redirect('hotel_menu/')
    return render(request, 'mainpage.html')

def hotelmenu(request):
    return render(request, 'page1.html')

def register_page(request):
    if request.method == "POST":    

        # The code for processing form data should be indented within the if block
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, "already registered")
            return redirect('/register_page/')

        user = User.objects.create(
            username=username,
            email=email,
        )

        # Set the password after creating the user
        user.set_password(password)
        user.save()
    
        messages.success(request, "Account created successfully")
    return render(request, 'register.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
            messages.error(request, "Invalid credential")
            return redirect('register_page')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid password")
            return redirect('login_page')
        
        login(request, user)
        return redirect('manager')

    return render(request, 'login.html')

@login_required(login_url='login_page/') # Specify the URL where users should be redirected if not logged in
def manager_site(request):
    return render(request, 'manager_site/manager_front_page.html')

def add_dish(request):
    if request.method == "POST":
        dish_type = request.POST.get('dishType')
        dish_name = request.POST.get('dishName')
        dish_price = request.POST.get('dishPrice')
        dish_description = request.POST.get('dishDescription')
        dish_image = request.FILES.get('dishImage')  # Use FILES for file uploads

        dish_instance = Dish(
            dish_type=dish_type,
            dish_name=dish_name,
            dish_price=dish_price,
            dish_description=dish_description,
            dish_image=dish_image
        )
        dish_instance.save()

        return redirect('add_dish')  # Redirect to the manager page after successful form submission

    return render(request, 'manager_site/add_dish.html')

def page1A(request):
    queryset = Dish.objects.filter(dish_type = 'appetizer')
    return render(request, 'page1A.html', {'items' : queryset})

def page2A(request):
    queryset = Dish.objects.filter(dish_type = 'mainCourse')
    Ingredients = DishIngredients.objects.filter(dish__dish_type = 'mainCourse')
    return render(request, 'page2A.html', {'items' : queryset, 'dish_ingredients': Ingredients})

def page3A(request):
    queryset = Dish.objects.filter(dish_type = 'dessert')
    return render(request, 'page3A.html', {'items' : queryset})


def page3A1(request):
    return render(request, 'page3A1.html')

@csrf_exempt
def cart(request):
    if request.method == "POST":
        try:
            # Parse the JSON data from the request body
            order_data = json.loads(request.body)
            totalAmount=0
            latest_customer = user_info.objects.order_by("-table_id").first()
            for item in order_data['items']:
                totalAmount += item['price'] * item['quantity']

            existing_order = Order.objects.filter(customer_id=latest_customer).first()
            customer_order = Order(
                customer_id=latest_customer,
                items=order_data,
                total_amount=totalAmount
            )
            customer_order.save()
            # Return a success response
            return JsonResponse({'success': True})
        except Exception as e:
            # Return an error response if there's any exception
            return JsonResponse({'success': False, 'error': str(e)})
    # For GET request, simply render the cart page
    return render(request, 'cart/cart.html')


def cook_site(request):
    
    # Get waiting orders
    waiting_orders = Order.objects.filter(is_order_completed=False)
    orders_data = {}
    for order in waiting_orders:
        # Assuming items field in Order model is a JSONField
        orders_data[order.customer_id.person_name] = order.items
    return render(request, 'cook/cook.html', {'waiting_orders':orders_data})