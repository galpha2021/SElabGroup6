from django.shortcuts import render
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import get_object_or_404, redirect

from django.contrib import messages
from django.db import IntegrityError
from django.db.models import F, Sum

from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Item, CustomShoppingCart, ShoppingCartItem, CustomOrder, OrderItem


# Register View
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        #print("Authenticated user:", user.username)
        if user is None:
            return render(request, 'login.html', {'error': 'Invalid username or password'})  
        else:
            login(request, user)
            return redirect('home') 
    
    return render(request, 'login.html')



def delete_account_view(request):
    if request.user.is_authenticated:
        #logout(request)
        request.user.delete()
        messages.success(request, "Account deleted.")
        return redirect('homepage')
    else:
        return redirect('login')





def register_view(request):
    US_STATES = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
        ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
        ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
        ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
        ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
        ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
        ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
        ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
        ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
        ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
        ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
    ]
    COUNTRIES = [
        ('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'),
        ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'),
        ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'),
        ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'),
        ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'),
        ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'),
        ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'),
        ('BR', 'Brazil'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'),
        ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'),
        ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'),
        ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CO', 'Colombia'),
        ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, the Democratic Republic of the'),
        ('CR', 'Costa Rica'), ('CI', 'Côte d\'Ivoire'), ('HR', 'Croatia'), ('CU', 'Cuba'),
        ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('DJ', 'Djibouti'),
        ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'),
        ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'),
        ('SZ', 'Eswatini'), ('ET', 'Ethiopia'), ('FJ', 'Fiji'), ('FI', 'Finland'),
        ('FR', 'France'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'),
        ('DE', 'Germany'), ('GH', 'Ghana'), ('GR', 'Greece'), ('GD', 'Grenada'),
        ('GT', 'Guatemala'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'),
        ('HT', 'Haiti'), ('HN', 'Honduras'), ('HU', 'Hungary'), ('IS', 'Iceland'),
        ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran'), ('IQ', 'Iraq'),
        ('IE', 'Ireland'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'),
        ('JP', 'Japan'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'),
        ('KI', 'Kiribati'), ('KP', 'Korea, Democratic People\'s Republic of'), ('KR', 'South Korea'),
        ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', 'Lao People\'s Democratic Republic'),
        ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'),
        ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'),
        ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'),
        ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MR', 'Mauritania'),
        ('MU', 'Mauritius'), ('MX', 'Mexico'), ('FM', 'Micronesia'), ('MD', 'Moldova'),
        ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MA', 'Morocco'),
        ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'),
        ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'),
        ('NE', 'Niger'), ('NG', 'Nigeria'), ('NO', 'Norway'), ('OM', 'Oman'),
        ('PK', 'Pakistan'), ('PW', 'Palau'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'),
        ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PL', 'Poland'),
        ('PT', 'Portugal'), ('QA', 'Qatar'), ('RO', 'Romania'), ('RU', 'Russian Federation'),
        ('RW', 'Rwanda'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'),
        ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'),
        ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'),
        ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'),
        ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'),
        ('ZA', 'South Africa'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'),
        ('SD', 'Sudan'), ('SR', 'Suriname'), ('SE', 'Sweden'), ('CH', 'Switzerland'),
        ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan'), ('TJ', 'Tajikistan'),
        ('TZ', 'Tanzania'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'),
        ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'),
        ('TM', 'Turkmenistan'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'),
        ('GB', 'United Kingdom'), ('US', 'United States'), ('UY', 'Uruguay'),
        ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela'), ('VN', 'Viet Nam'),
        ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe'),
    ]
    

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        retypepassword = request.POST['retypepassword']
        name = request.POST['name']
        credit_card_number = request.POST['creditcard']
        expiration_date = request.POST['expirationdate']
        security_code = request.POST['securitycode']
        street_address = request.POST['streetAddress']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip']
        email = request.POST['email']
        role = request.POST['accountType']
        country = request.POST['country']

        if password != retypepassword:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html', {'states': US_STATES, 'countries': COUNTRIES})

        try:
            CustomUser = get_user_model()
            CustomUser.objects.create_user(
                username=username,
                password=password,
                first_name=name,
                credit_card_number=credit_card_number,
                expiration_date=expiration_date,
                security_code=security_code,
                street_address=street_address,
                city=city,
                state=state,
                zip_code=zip_code,
                email=email,
                role=role,
                country=country
            )
            messages.success(request, "Account created successfully!")
            return redirect('login')

        except IntegrityError:
            messages.error(request, "Username already exists. Please choose a different one.")
            return render(request, 'register.html', {'states': US_STATES, 'countries': COUNTRIES})


        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return render(request, 'register.html', {'states': US_STATES, 'countries': COUNTRIES})


    return render(request, 'register.html', {'states': US_STATES, 'countries': COUNTRIES})





@login_required
def seller_dashboard(request):
    items = Item.objects.filter(vendor=request.user)
    orders = CustomOrder.objects.prefetch_related('order_items__item').filter(order_items__item__vendor=request.user).distinct()
    totals = []

    for order in orders:
        for item in order.order_items.all():
            if item.item.vendor == request.user:
                total = item.item.price * item.quantity
                totals.append({
                    'order_id': order.order_id,
                    'buyer_id': order.user.id,
                    'date': order.ordertime,
                    'item': item.item.name,
                    'quantity': item.quantity,
                    'total_earned': total
                })
                
    return render(request, 'seller.html', {
    'items': items,
    'orders': orders,
    'sales_data': totals
})


def logout_view(request):
    if request.method == 'POST':
        return render(request, 'loggedout.html')  
    return render(request, 'logout.html')  




def loggedout_view(request):
    logout(request)
    return render(request, 'loggedout.html')

@login_required
def update_view(request):
    print("Update.html page vistited")
    US_STATES = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
        ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
        ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
        ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
        ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
        ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
        ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
        ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
        ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
        ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
        ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
    ]
    COUNTRIES = [
        ('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'),
        ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'),
        ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'),
        ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'),
        ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'),
        ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'),
        ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'),
        ('BR', 'Brazil'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'),
        ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'),
        ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'),
        ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CO', 'Colombia'),
        ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, the Democratic Republic of the'),
        ('CR', 'Costa Rica'), ('CI', 'Côte d\'Ivoire'), ('HR', 'Croatia'), ('CU', 'Cuba'),
        ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('DJ', 'Djibouti'),
        ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'),
        ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'),
        ('SZ', 'Eswatini'), ('ET', 'Ethiopia'), ('FJ', 'Fiji'), ('FI', 'Finland'),
        ('FR', 'France'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'),
        ('DE', 'Germany'), ('GH', 'Ghana'), ('GR', 'Greece'), ('GD', 'Grenada'),
        ('GT', 'Guatemala'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'),
        ('HT', 'Haiti'), ('HN', 'Honduras'), ('HU', 'Hungary'), ('IS', 'Iceland'),
        ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran'), ('IQ', 'Iraq'),
        ('IE', 'Ireland'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'),
        ('JP', 'Japan'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'),
        ('KI', 'Kiribati'), ('KP', 'Korea, Democratic People\'s Republic of'), ('KR', 'South Korea'),
        ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', 'Lao People\'s Democratic Republic'),
        ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'),
        ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'),
        ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'),
        ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MR', 'Mauritania'),
        ('MU', 'Mauritius'), ('MX', 'Mexico'), ('FM', 'Micronesia'), ('MD', 'Moldova'),
        ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MA', 'Morocco'),
        ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'),
        ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'),
        ('NE', 'Niger'), ('NG', 'Nigeria'), ('NO', 'Norway'), ('OM', 'Oman'),
        ('PK', 'Pakistan'), ('PW', 'Palau'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'),
        ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PL', 'Poland'),
        ('PT', 'Portugal'), ('QA', 'Qatar'), ('RO', 'Romania'), ('RU', 'Russian Federation'),
        ('RW', 'Rwanda'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'),
        ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'),
        ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'),
        ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'),
        ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'),
        ('ZA', 'South Africa'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'),
        ('SD', 'Sudan'), ('SR', 'Suriname'), ('SE', 'Sweden'), ('CH', 'Switzerland'),
        ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan'), ('TJ', 'Tajikistan'),
        ('TZ', 'Tanzania'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'),
        ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'),
        ('TM', 'Turkmenistan'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'),
        ('GB', 'United Kingdom'), ('US', 'United States'), ('UY', 'Uruguay'),
        ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela'), ('VN', 'Viet Nam'),
        ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe'),
    ]
    return render(request, 'update.html', {'states': US_STATES, 'countries': COUNTRIES})
    

@login_required
def update_updatedb(request):
    if request.method == "POST":
        credit_card_number = request.POST['creditcard']
        expiration_date = request.POST['expirationdate']
        security_code = request.POST['securitycode']
        street_address = request.POST['streetAddress']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip']
        countries=request.POST['countries']

        user=request.user
        user.credit_card_number=credit_card_number
        user.expiration_date=expiration_date
        user.security_code=security_code
        user.street_address=street_address
        user.city=city
        user.state=state
        user.zip_code=zip_code
        user.countries=countries
        user.save()   
        messages.success(request, "Account updated successfully!")
    return redirect(request, "homepage.html")




@login_required
def add_item(request):
    valid_extensions = ('.jpg', '.gif', '.png', '.svg', '.pjp', '.pjpeg', '.jfif', '.webp', '.avif', '.tif', '.tiff', '.bmp', '.ico', '.cur')

    if request.method == 'POST':
        name = request.POST.get('itemName')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        try:
            price = float(request.POST.get('price'))
            quantity = int(request.POST.get('quantity'))
        except (TypeError, ValueError):
            messages.error(request, "Price must be a number and quantity must be an integer.")
            return redirect('seller')

        # Validate image extension
        if image and not image.name.lower().endswith(valid_extensions):
            messages.error(request, "Invalid image file type.")
            return redirect('seller')

        # Validate values
        if price < 0 or quantity < 0:
            messages.error(request, "Price and quantity must be non-negative.")
            return redirect('seller')

        if name and price is not None and quantity is not None and image:
            Item.objects.create(
                name=name,
                price=price,
                description=description,
                stock=quantity,
                item_photo=image,
                vendor=request.user
            )
            messages.success(request, "Item listed successfully.")
        else:
            messages.error(request, "All fields are required.")

        return redirect('seller')

    return redirect('home')


def seller_update_or_delete(request):
    valid_extensions = ('.jpg', '.gif', '.png', '.jpg', '.svg', '.pjp', '.pjpeg', '.jfif', '.webp', '.avif', '.tif', '.tiff', 'bmp', '.ico', '.cur')

    if request.method == "POST":
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        if not item_id:
            return redirect('seller')

        try:
            item = Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return redirect('seller')  

        if action == "delete":
            item.delete()

        elif action == "update":
            
            name = request.POST.get('name')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            if name: item.name = name
            if price: item.price = float(price)
            if stock: item.stock = int(stock)
            if description: item.description = description
            print(f"The Image type is: {type(image)}")
            print(f"The Image is: {image}")
            if image: 
                if not image.name.endswith(valid_extensions):
                    return redirect('seller')
                item.item_photo = image

            if item.price < 0:
                return redirect('seller')
            if item.stock < 0:
                return redirect('seller')
            
            item.save()

    return redirect('seller')


def homepage_view(request):
    items = Item.objects.all()
    return render(request, 'homepage.html', {'items': items})
@login_required
def view_checkout(request):
    return render(request, 'Checkout.html')
@login_required
def view_transactions(request):
    return render(request, 'Transaction.html')


@login_required
def add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, item_id=item_id)
        print(f"Item Stock: {item.stock}")
        if item.stock <= 0:
            messages.error(request, f"Could not add item! Out of Stock!")
            return redirect('home')

        cart, created = CustomShoppingCart.objects.get_or_create(user=request.user)
        cart_item, created = ShoppingCartItem.objects.get_or_create(cart=cart, item=item)

        user_bal=request.user.account_balance
        item_price=item.price
        cart_items = ShoppingCartItem.objects.filter(cart=cart)
        current_cart_cost = cart_items.aggregate(total=Sum(F('quantity') * F('item__price')))['total'] or 0

        newCartprice=current_cart_cost+item_price

        if newCartprice > user_bal:
            messages.error(request, f"Invalid add! Item is too expensive!")
            return redirect('home')

        if created:
            # newly added to cart, quantity is already 1
            pass
        else:
            if cart_item.quantity + 1 > item.stock:
                messages.error(request, f"Not enough stock available.")
                return redirect('home')
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, f"{item.name} added to cart!")
        return redirect('home')
        
    else:
        return redirect('home')




def view_cart(request):
    cart, _ = CustomShoppingCart.objects.get_or_create(user=request.user)
    cart_items = ShoppingCartItem.objects.filter(cart=cart)
    users_bal=request.user.account_balance
    total = 0
    

    for item in cart_items:
        item_total = item.quantity * item.item.price
        total += item_total
    new_user_balance= users_bal-total

        

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total,
        'new_user_bal': new_user_balance
    })

@login_required
def remove_from_cart(request):
    item_id = request.POST.get('item_id')
    cart, _ = CustomShoppingCart.objects.get_or_create(user=request.user)
    item = get_object_or_404(Item, item_id=item_id)
    
    try:
        cart_item = ShoppingCartItem.objects.get(cart=cart, item=item)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        messages.success(request, f"Removed one {item.name} from cart.")
    except ShoppingCartItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")

    return redirect('view_cart')
@login_required
def admin_monitor_users(request):
    if request.user.role != 'Admin':
        return redirect('home')  
    users = User.objects.all() 
    return render(request, 'admin_monitor_users.html', {'users': users})


def admin_monitor_products(request):
    if request.user.role != 'Admin':
        return redirect('home')  
    products = Item.objects.all()  
    return render(request, 'admin_monitor_products.html', {'products': products})


def admin_delete_account(request, user_id):
    if request.user.role != 'Admin':
        return redirect('home')  
    try:
        user = User.objects.get(id=user_id)
        user.delete()  
        messages.success(request, "Account successfully deleted.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")
    return redirect('admin_monitor_users')


@login_required
def checkout(request):
    cart, _ = CustomShoppingCart.objects.get_or_create(user=request.user)
    cart_items = ShoppingCartItem.objects.filter(cart=cart)

    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    total_cost = sum(item.quantity * item.item.price for item in cart_items)

    if request.user.account_balance < total_cost:
        messages.error(request, "Insufficient funds.")
        return redirect('view_cart')

    # Deduct user balance
    request.user.account_balance -= total_cost
    request.user.save()

    # Create order record
    order = CustomOrder.objects.create(
        user=request.user,
        order_cost=total_cost,
        shipping_street_address=request.user.street_address,
        shipping_city=request.user.city,
        shipping_state=request.user.state,
        shipping_zip_code=request.user.zip_code,
    )

    # Move cart items to order and pay sellers
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            item=cart_item.item,
            quantity=cart_item.quantity
        )

        seller = cart_item.item.vendor
        seller.account_balance += cart_item.quantity * cart_item.item.price
        seller.save()

        # Optionally update stock
        cart_item.item.stock -= cart_item.quantity
        cart_item.item.save()

    # Clear the cart
    cart_items.delete()

    messages.success(request, "Checkout successful. Thank you for your purchase.")
    return redirect('home')


def search_items(request):
    query = request.GET.get('q', '')
    items = Item.objects.filter(name__icontains=query)
    return render(request,'item_list.html',{'items': items})

@login_required
def view_Terms(request):
    return render(request, 'Terms and Services.html')






    