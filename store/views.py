import django
import razorpay
import json
import hmac
import hashlib
import uuid
from django.contrib.auth.models import User
from store.models import Address, Cart, Category, Order, Product, Payment
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm, AddressForm
from django.contrib import messages
from django.views import View
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator # for Class Based Views
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q, F, Sum, DecimalField, ExpressionWrapper
from .context_preprocessors import (
    clear_cart_count_for_request,
    get_cart_count_for_request,
    set_cart_count_for_request,
)
from .email_utils import (
    send_order_admin_alert,
    send_order_email,
    send_password_change_admin_alert,
    send_password_change_email,
    send_registration_admin_alert,
    send_registration_email,
)


# Create your views here.

def home(request):
    categories = Category.objects.filter(is_active=True, is_featured=True).only('title', 'slug', 'category_image')[:3]
    products = (
        Product.objects.filter(is_active=True, is_featured=True)
        .select_related('category')
        .only('title', 'slug', 'price', 'product_image', 'category__slug')[:8]
    )
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/index.html', context)


def detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category').only(
            'title',
            'slug',
            'sku',
            'short_description',
            'detail_description',
            'product_image',
            'price',
            'category__slug',
            'category__title',
        ),
        slug=slug,
    )
    related_products = (
        Product.objects.exclude(id=product.id)
        .filter(is_active=True, category=product.category)
        .select_related('category')
        .only('title', 'slug', 'price', 'product_image', 'category__slug')
    )
    context = {
        'product': product,
        'related_products': related_products,

    }
    return render(request, 'store/detail.html', context)


def all_categories(request):
    categories = Category.objects.filter(is_active=True).only('title', 'slug', 'category_image')
    return render(request, 'store/categories.html', {'categories':categories})


def category_products(request, slug):
    category = get_object_or_404(Category.objects.only('id', 'title', 'slug'), slug=slug)
    products = (
        Product.objects.filter(is_active=True, category=category)
        .select_related('category')
        .only('title', 'slug', 'price', 'product_image', 'category__slug')
    )
    categories = Category.objects.filter(is_active=True).only('title', 'slug')
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/category_products.html', context)


# Authentication Starts Here

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'account/register.html', {'form': form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_registration_email(user)
            send_registration_admin_alert(user)
            messages.success(request, "Congratulations! Registration Successful!")
            return redirect('store:login')
        return render(request, 'account/register.html', {'form': form})
        

@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user).only('locality', 'city', 'state')
    orders = (
        Order.objects.filter(user=request.user)
        .select_related('product')
        .only('status', 'ordered_date', 'quantity', 'product__title')
    )
    return render(request, 'account/profile.html', {'addresses':addresses, 'orders':orders})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, 'account/add_address.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user=request.user
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            reg = Address(user=user, locality=locality, city=city, state=state)
            reg.save()
            messages.success(request, "New Address Added Successfully.")
        return redirect('store:profile')


@login_required
def remove_address(request, id):
    a = get_object_or_404(Address, user=request.user, id=id)
    a.delete()
    messages.success(request, "Address removed.")
    return redirect('store:profile')


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    """
    Custom logout view that displays a confirmation page
    GET: Shows logout confirmation page
    POST: Logs out the user and redirects to logout success page
    """
    def get(self, request):
        return render(request, 'account/logout.html')
    
    def post(self, request):
        auth_logout(request)
        messages.success(request, "You have been successfully logged out!")
        return render(request, 'account/logout_success.html')


class PasswordChangeNotifyView(auth_views.PasswordChangeView):
    def form_valid(self, form):
        response = super().form_valid(form)
        send_password_change_email(self.request.user)
        send_password_change_admin_alert(self.request.user)
        messages.success(self.request, "Your password was changed successfully.")
        return response


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    # Check whether the Product is alread in Cart or Not
    cart_item = Cart.objects.filter(product=product, user=user).first()
    if cart_item:
        cp = cart_item
        cp.quantity += 1
        cp.save()
    else:
        Cart.objects.create(user=user, product=product)
        set_cart_count_for_request(request, get_cart_count_for_request(request) + 1)

    cart_count = get_cart_count_for_request(request)
    is_ajax_request = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax_request:
        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'message': 'Added to cart',
        })

    redirect_target = request.META.get('HTTP_REFERER') or '/cart/'
    return redirect(redirect_target)


@login_required
def cart(request):
    user = request.user
    cart_products = (
        Cart.objects.filter(user=user)
        .select_related('product')
        .only('quantity', 'product__title', 'product__slug', 'product__price', 'product__product_image')
    )

    # Display Total on Cart Page
    shipping_amount = decimal.Decimal(10)
    amount = cart_products.aggregate(
        total=Sum(
            ExpressionWrapper(
                F('quantity') * F('product__price'),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        )
    )['total'] or decimal.Decimal(0)

    # Customer Addresses
    addresses = Address.objects.filter(user=user).only('locality', 'city', 'state')

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
    }
    return render(request, 'store/cart.html', context)


@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id, user=request.user)
        c.delete()
        set_cart_count_for_request(request, max(get_cart_count_for_request(request) - 1, 0))
        messages.success(request, "Product removed from Cart.")
    return redirect('store:cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id, user=request.user)
        cp.quantity += 1
        cp.save()
    return redirect('store:cart')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id, user=request.user)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
            set_cart_count_for_request(request, max(get_cart_count_for_request(request) - 1, 0))
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('store:cart')


@login_required
def checkout(request):
    """Redirect to payment page with selected address"""
    user = request.user
    address_id = request.GET.get('address')
    payment_method = request.GET.get('payment', 'online')
    
    try:
        address = get_object_or_404(Address, id=address_id, user=user)
    except:
        messages.error(request, "Please select a valid address.")
        return redirect('store:cart')
    
    # Get cart items
    cart_items = Cart.objects.filter(user=user)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('store:cart')
    
    # Calculate total amount
    shipping_amount = decimal.Decimal(10)
    total_amount = cart_items.aggregate(
        total=Sum(
            ExpressionWrapper(
                F('quantity') * F('product__price'),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        )
    )['total'] or decimal.Decimal(0)
    total_amount += shipping_amount
    
    # Store in session for payment processing
    request.session['cart_items'] = list(cart_items.values_list('id', flat=True))
    request.session['address_id'] = address_id
    request.session['total_amount'] = str(total_amount)
    
    if payment_method == 'cod':
        # Cash on Delivery - Create orders directly
        return process_cod_order(request, cart_items, address)
    else:
        # Online Payment - Redirect to payment page
        return redirect('store:payment')


def process_cod_order(request, cart_items, address):
    """Process Cash on Delivery order"""
    user = request.user
    try:
        for cart_item in cart_items:
            order = Order(
                user=user,
                address=address,
                product=cart_item.product,
                quantity=cart_item.quantity,
                payment_status=False
            )
            order.save()
            send_order_email(order, status_label="Order placed")
            send_order_admin_alert(order, action_label="New COD order placed")
            cart_item.delete()
        
        clear_cart_count_for_request(request)
        messages.success(request, "Order placed successfully! You will pay on delivery.")
        return redirect('store:orders')
    except Exception as e:
        messages.error(request, f"Error processing order: {str(e)}")
        return redirect('store:cart')


def _create_paid_orders(request, cart_items, address, *, razorpay_order_id, razorpay_payment_id, razorpay_signature):
    user = request.user

    for cart_item in cart_items:
        order = Order(
            user=user,
            address=address,
            product=cart_item.product,
            quantity=cart_item.quantity,
            payment_status=True,
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
        )
        order.save()
        send_order_email(order, status_label="Payment received and order placed")
        send_order_admin_alert(order, action_label="New paid order placed")
        cart_item.delete()


def _clear_payment_session(request):
    for key in ('cart_items', 'address_id', 'total_amount', 'razorpay_order_id'):
        if key in request.session:
            del request.session[key]


@login_required
def payment(request):
    """Display payment page with Razorpay checkout"""
    user = request.user
    
    # Get data from session
    cart_item_ids = request.session.get('cart_items', [])
    address_id = request.session.get('address_id')
    total_amount = decimal.Decimal(request.session.get('total_amount', 0))
    
    if not cart_item_ids or not address_id:
        messages.error(request, "Session expired. Please try again.")
        return redirect('store:cart')
    
    try:
        address = Address.objects.get(id=address_id, user=user)
        cart_items = (
            Cart.objects.filter(id__in=cart_item_ids, user=user)
            .select_related('product')
            .only('quantity', 'product__title', 'product__slug', 'product__price', 'product__product_image')
        )
        
        if not cart_items.exists():
            messages.error(request, "Cart items not found.")
            return redirect('store:cart')
        
        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        
        # Create Razorpay order
        razorpay_order = client.order.create(dict(
            amount=int(total_amount * 100),  # Amount in paise
            currency=settings.RAZORPAY_CURRENCY,
            payment_capture='0'
        ))
        
        # Store order details in session
        request.session['razorpay_order_id'] = razorpay_order['id']
        
        context = {
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'razorpay_order_id': razorpay_order['id'],
            'amount': int(total_amount * 100),
            'user_name': user.get_full_name() or user.username,
            'user_email': user.email,
            'user_phone': user.username,
            'currency': settings.RAZORPAY_CURRENCY,
            'cart_items': cart_items,
            'address': address,
            'total_amount': total_amount,
            'payment_countdown_seconds': settings.PAYMENT_SIMULATION_SECONDS,
            'enable_payment_simulation': settings.ENABLE_PAYMENT_SIMULATION,
        }
        
        return render(request, 'store/payment.html', context)
    
    except Address.DoesNotExist:
        messages.error(request, "Address not found.")
        return redirect('store:cart')
    except Exception as e:
        messages.error(request, f"Error initiating payment: {str(e)}")
        return redirect('store:cart')


@login_required
def payment_verify(request):
    """Verify Razorpay payment and create orders"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    try:
        data = json.loads(request.body)
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        simulate_payment = data.get('simulate_payment', False)

        if simulate_payment:
            razorpay_payment_id = razorpay_payment_id or f'sim_{uuid.uuid4().hex}'
            razorpay_signature = razorpay_signature or 'SIMULATED'
        
        if not simulate_payment:
            # Verify signature
            signature_data = f'{razorpay_order_id}|{razorpay_payment_id}'
            expected_signature = hmac.new(
                settings.RAZORPAY_SECRET_KEY.encode(),
                signature_data.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if expected_signature != razorpay_signature:
                return JsonResponse({'error': 'Payment verification failed'}, status=400)
        
        # Get cart data from session
        user = request.user
        cart_item_ids = request.session.get('cart_items', [])
        address_id = request.session.get('address_id')
        
        if not cart_item_ids or not address_id:
            return JsonResponse({'error': 'Session expired'}, status=400)
        
        address = Address.objects.get(id=address_id, user=user)
        cart_items = Cart.objects.filter(id__in=cart_item_ids, user=user).select_related('product')
        
        # Create orders and update payment status
        _create_paid_orders(
            request,
            cart_items,
            address,
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
        )
        
        # Clear session
        _clear_payment_session(request)
        clear_cart_count_for_request(request)
        
        return JsonResponse({'success': True, 'redirect_url': '/orders/'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def payment_failure(request):
    """Handle payment failure"""
    messages.error(request, "Payment failed. Please try again.")
    return redirect('store:cart')


@login_required
def orders(request):
    all_orders = (
        Order.objects.filter(user=request.user)
        .select_related('product')
        .only('status', 'ordered_date', 'quantity', 'product__title', 'product__product_image')
        .order_by('-ordered_date')
    )
    return render(request, 'store/orders.html', {'orders': all_orders})


def shop(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    products = Product.objects.filter(is_active=True).select_related('category').only(
        'title',
        'slug',
        'price',
        'product_image',
        'short_description',
        'sku',
        'detail_description',
        'category__title',
        'category__slug',
    )

    if query:
        products = products.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(detail_description__icontains=query)
            | Q(sku__icontains=query)
            | Q(category__title__icontains=query)
            | Q(category__description__icontains=query)
        )

    selected_category = None
    if category_slug:
        products = products.filter(category__slug=category_slug)
        selected_category = Category.objects.filter(is_active=True, slug=category_slug).only('title', 'slug').first()

    categories = Category.objects.filter(is_active=True).only('title', 'slug')

    context = {
        'products': products.distinct().order_by('-created_at'),
        'categories': categories,
        'query': query,
        'selected_category': selected_category,
        'results_count': products.count(),
    }
    return render(request, 'store/shop.html', context)


def test(request):
    return render(request, 'store/test.html')


# Policy and Info Pages
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not message:
            messages.error(request, "Please fill in all required fields.")
            return redirect('store:contact')

        subject = f"New Contact Form Message from {name}"
        plain_body = (
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone or 'Not provided'}\n\n"
            f"Message:\n{message}"
        )

        html_body = render_to_string(
            'emails/contact_notification.html',
            {
                'name': name,
                'email': email,
                'phone': phone or 'Not provided',
                'message': message,
            }
        )

        try:
            email_message = EmailMultiAlternatives(
                subject=subject,
                body=plain_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_RECEIVER_EMAIL],
                reply_to=[email],
            )
            email_message.attach_alternative(html_body, "text/html")
            email_message.send(fail_silently=False)
            messages.success(request, "Thank you for contacting us! Your message has been sent successfully.")
        except Exception as e:
            if settings.DEBUG:
                messages.error(request, f"Unable to send your message right now: {e}")
            else:
                messages.error(request, "Unable to send your message right now. Please try again later.")

        return redirect('store:contact')
    
    return render(request, 'store/contact.html')


def shipping_policy(request):
    return render(request, 'store/shipping_policy.html')


def privacy_policy(request):
    return render(request, 'store/privacy_policy.html')


def return_policy(request):
    return render(request, 'store/return_policy.html')


def terms_conditions(request):
    return render(request, 'store/terms_conditions.html')