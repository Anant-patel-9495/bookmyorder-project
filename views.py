from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from OnlineRestaurant.mainpage import *
from OnlineRestaurant.hotelmenu import *
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http import JsonResponse
import json
from django.utils import timezone
from OnlineRestaurant.hotelmenu import bill_site

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

@login_required(login_url='login_page') # Specify the URL where users should be redirected if not logged in
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

def export_customer_data(request):
    orders = Order.objects.all()
    # Create a list to hold all orders
    all_orders = []

    # Iterate through the orders and convert them to a dictionary
    for order in orders:
        all_orders.append(order.items)
    
    total_quantities = {}

    for order in all_orders:
        for item in order:
            name = item.get('name')
            quantity = item.get('quantity')
            if name and quantity:
                if name in total_quantities:
                    total_quantities[name] += quantity
                else:
                    total_quantities[name] = quantity
    print(total_quantities)
            

    return render(request, 'manager_site/top_seller.html', {'total_quantities' : total_quantities})

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
            order_data = json.loads(request.body.decode('utf-8'))

            # Get the latest customer
            latest_customer = user_info.objects.order_by("-table_id").first()
            print(latest_customer)

            # Calculate the total amount of the order
            Total_amount = 0
            for item in order_data:
                Total_amount += item['price'] * item['quantity']

            # Check if there's an existing order for the customer
            existing_order = Order.objects.filter(customer_id=latest_customer).first()
            print(existing_order)
            if existing_order and not existing_order.is_order_completed:
                # Update the existing order with new items and total amount
                existing_order.items.extend(order_data)
                existing_order.total_amount += Total_amount
                existing_order.save()
            else:
                # Create a new order if it doesn't exist
                customer_order = Order.objects.create(
                    customer_id=latest_customer,
                    items=order_data,
                    total_amount=Total_amount
                )


            # Return a success response
            return JsonResponse({'success': True})

        except Exception as e:
            print("Exception:", e)
            return JsonResponse({'success': False, 'error': str(e)})

    # For GET request, simply render the cart page
    return render(request, 'cart/cart.html')

def cook_site(request):
    if request.method == "POST":
        person = request.POST.get("person")
        person_id = person.split(" ")[0]
        order = Order.objects.get(customer_id=person_id)
        order.is_order_completed = True
        order.save()


    waiting_orders = Order.objects.filter(is_order_completed=False)
    print(waiting_orders)
    order_id = []
    orders_data = {}
    for order in waiting_orders:
        # Assuming items field in Order model is a JSONField
        order_id.append(order.customer_id.table_id)
        person = f"{order.customer_id.table_id} - {order.customer_id.person_name}"
        orders_data[person] = order.items
    return render(request, 'cook/cook.html', {'waiting_orders':orders_data})

def user_bill(request):
    latest_customer = user_info.objects.order_by("-table_id").first()
    existing_order = Order.objects.filter(customer_id=latest_customer).first()
    print(existing_order.items)
    return render(request, 'bill_site/user_bill.html', {'existing_order' : existing_order})