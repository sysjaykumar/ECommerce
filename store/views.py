from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem, Order
from django.contrib.auth.decorators import login_required

# Display product list
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# Add product to cart
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

# View cart details
@login_required
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'store/cart_detail.html', {'cart': cart})

# Checkout and create an order
@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart.items.all())
    order = Order.objects.create(user=request.user, total_price=total_price)
    order.items.set(cart.items.all())
    order.save()
    cart.items.clear()  # Empty the cart after checkout
    return redirect('order_detail', order_id=order.id)

# Order details
@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'store/order_detail.html', {'order': order})
