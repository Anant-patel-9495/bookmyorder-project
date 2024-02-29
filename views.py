from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from OnlineRestaurant.mainpage import *
from OnlineRestaurant.hotelmenu import *
import random
from .models import *

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

def cart(request):
    return render(request, 'cart/cart.html')


def page3A1(request):
    return render(request, 'page3A1.html')




def create_order(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data sent from cart.js
            data = json.loads(request.body)

            # Extract the relevant information from the data
            last_user_table_id = user_info.objects.latest('table_id').table_id
            items = data.get('items')
            total_amount = data.get('total_amount')

            # Retrieve user_info instance based on customer_id
            user_info_instance = user_info.objects.get(pk=last_user_table_id)

            # Create the Order instance
            order = Order.objects.create(
                customer_id=user_info_instance,
                items=items,
                total_amount=total_amount
                # Add more fields as needed
            )

            # Return a success response
            return JsonResponse({'success': True})
        except user_info.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'No user_info instance found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})