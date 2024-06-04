from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Feedback, Product,Cart

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user )
            messages.success(request, 'Logged in successfully.')

            if user.is_superuser:
                return redirect('admins')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['mail']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if not (name and email and password and confirm_password):
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.save()
            return redirect('login_user')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return redirect('register')

    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    products = Product.objects.all()
    return render(request, 'User_dashboard.html',{'product': products})

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html',{})

#function to add product through the admin page
@login_required
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('productName')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if product_name and price and description and image:
            try:
                price = int(price)
            except ValueError:
                messages.error(request, 'Price must be a valid number.')
                return redirect('admins')

            if not image.content_type.startswith('image'):
                messages.error(request, 'Please upload a valid image file.')
                return redirect('admins')
            
            product = Product.objects.create(name=product_name, price=price, description=description, image=image)
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('admins')
        else:
            messages.error(request, 'Please fill in all fields.')
            return redirect('admins')

    return render(request, 'add_product.html')

#functoin to view the item added in the cart
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

#function to add the item in the cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, 'Product added Successfully!', extra_tags='cart-success')
        
    return redirect('home')

#function to remove the item of the cart
@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item = get_object_or_404(Cart, user=request.user, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    messages.success(request, "Item removed sucessfully")
    return redirect('view_cart')

#function to clear the whole cart on click
@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.products.clear()
    return redirect('view_cart')

# function to view the added product on the admin page
@login_required
def view_product(request):
    product = Product.objects.all()
    return render(request,'view_product.html',{'product':product})    

# function to delete added product 
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, product_ID=product_id)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('view_product')
    
    return render(request, 'view_product.html', {'product': product})  

@login_required
def feedback_page(request):
    return render(request, 'feedback.html')

@login_required
def feedback_from(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        if feedback_text:
            feedback = Feedback(user=request.user, feedback_text=feedback_text)
            feedback.save()
            messages.success(request, 'form submitted sucessfully')
        return redirect('feedback')
    
@login_required
def view_feedback(request):
    feedback = Feedback.objects.all
    return render(request,'view_feedback.html',{'feedback':feedback})    
