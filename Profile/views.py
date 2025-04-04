from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
import random
from django.core.mail import send_mail
# Create your views here.
from jdatetime import datetime
from django.conf import settings
from Profile.models import Tickets, AnswerTicket, Address
from Account.models import CustomUser
from django.contrib.auth.decorators import login_required
from Shop.models import Product, FavoriteProduct, Cart, ProductCart, CommentsProduct, StarProduct
from ipware import get_client_ip


@login_required
def profile_dashboard(request):
    # for show dashboard
    if request.method == 'POST':
        x = ''.join((random.choice('0123456789') for _ in range(5)))  # Creating a verification code
        request.session['username'] = request.user.username
        user = CustomUser.objects.get(pk=request.user.pk)
        user.verify_code = x
        user.save()
        send_mail(subject='moji', message='hi moji ' + x, from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[request.user.email])  # Send email
        return redirect('verify_email')
    # Getting four of the favorites
    my_favorites = FavoriteProduct.objects.using('shop').filter(user_id=request.user.pk, user=request.user)[:4]
    # Getting four of the favorites product
    my_favorites = Product.objects.filter(pk__in=my_favorites.values('product_id'))
    # View shopping cart
    carts = Cart.objects.filter(user_id=request.user.pk, user=request.user)
    # Get user to display user information
    myuser = CustomUser.objects.get(pk=request.user.pk)
    context = {'myuser': myuser, 'my_favorites': my_favorites, 'carts': carts}
    return render(request, 'front/Profile/profile_dashboard.html', context=context)


@login_required
def profile_user_history(request):
    # for see user history
    myuser = CustomUser.objects.get(pk=request.user.pk)
    context = {'myuser': myuser}
    if 'product_view' in request.session:  # Getting hits from sessions
        product_view = request.session['product_view']
        products_view = Product.objects.filter(name_product__in=product_view)
        context['products_view'] = products_view
    return render(request, 'front/Profile/profile_user_history.html', context=context)


@login_required
def profile_comments(request):
    # for see all comments user
    comments = CommentsProduct.objects.filter(user_id=request.user.pk, user=request.user)
    products_comment = Product.objects.filter(pk__in=comments.values_list('pk_product', flat=True))
    my_stars=StarProduct.objects.filter(user=request.user.username)
    myuser = CustomUser.objects.get(pk=request.user.pk)
    context = {'myuser': myuser, 'comments': comments, 'products_comment': products_comment,'my_stars':my_stars}
    return render(request, 'front/Profile/profile_comments.html', context=context)


@login_required
def profile_personal_info(request):
    # Viewing the user's personal information and editing it
    myuser = CustomUser.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        last_name = request.POST.get('lname')
        first_name = request.POST.get('fname')
        phone_number = request.POST.get('phone_number')
        national_number = request.POST.get('national_number')
        card_number = request.POST.get('card_number')
        image = request.FILES.get('image')
        email = request.POST.get('email')
        myuser.last_name = last_name
        myuser.first_name = first_name
        myuser.phone_number = phone_number
        myuser.national_number = national_number
        myuser.card_number = card_number
        if image:
            myuser.image = image
        if email != myuser.email:  # When the email changes, it must be confirmed
            x = ''.join((random.choice('0123456789') for _ in range(5)))
            # Creating a verification code
            request.session['username'] = request.user.username
            myuser.verify_code = x
            myuser.is_active = False  # Save as inactive
            myuser.email = email
            myuser.save()
            send_mail(subject='moji', message='hi moji ' + x, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[email])  # Send email
            return redirect('verify_email')
        else:
            myuser.save()
            return redirect('profile_personal_info')

    return render(request, 'front/Profile/profile_personal_info.html', {'myuser': myuser, })


@login_required
def profile_address(request):
    # for show addresses
    addresses = Address.objects.filter(user_id=request.user.pk, user=request.user)
    myuser = CustomUser.objects.get(pk=request.user.pk)
    return render(request, 'front/Profile/profile_address.html', {'addresses': addresses, 'myuser': myuser})


@login_required
def profile_add_address(request):
    # for add new address
    if request.method == 'POST':
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        name = request.POST.get('name')
        postal_code = request.POST.get('postal_code')
        # add address
        new_address = Address(city=city, state=state, phone=phone, address=address, name=name, postal_code=postal_code,
                              user=request.user, user_id=request.user.pk, status=1)
        address = Address.objects.filter(user=request.user, user_id=request.user.pk)
        address.update(status=0)  # Changing the active address for sending goods
        new_address.save(using='profile')

        return redirect(request.META['HTTP_REFERER'])


@login_required
def profile_edit_address(request, pk):
    # for edit address
    if request.method == 'POST':
        edit_city = request.POST.get('edit_city')
        edit_state = request.POST.get('edit_state')
        edit_phone = request.POST.get('edit_phone')
        edit_address = request.POST.get('edit_address')
        edit_name = request.POST.get('edit_name')
        edit_postal_code = request.POST.get('edit_postal_code')
        edit_new_address = Address.objects.get(pk=pk)
        edit_new_address.city = edit_city
        edit_new_address.state = edit_state
        edit_new_address.phone = edit_phone
        edit_new_address.address = edit_address
        edit_new_address.name = edit_name
        edit_new_address.postal_code = edit_postal_code
        edit_new_address.save(using='profile')
        return redirect(request.META['HTTP_REFERER'])


@login_required
def profile_delete_address(request, pk):
    # for delete address
    edit_new_address = Address.objects.get(pk=pk)
    edit_new_address.delete(using='profile')
    return redirect(request.META['HTTP_REFERER'])


@login_required
def profile_tickets(request):
    # Send a ticket by the user
    if not request.user.is_active:  # Account activation notification
        messages.warning(request, 'Please activate your account')
        return redirect('profile_dashboard')

    myuser = CustomUser.objects.get(pk=request.user.pk)
    parts = Group.objects.all()  # To display different sections for sending tickets
    tickets = Tickets.objects.using('profile').order_by('-date').filter(user_id=request.user.pk)
    for i in tickets.filter(status='درحال بررسی'):
        # If a ticket is more than ten days old, it will be closed
        if ((int(datetime.now().year) * 365) + (int(datetime.now().month) * 30) + (int(datetime.now().day))) - (
                (int(i.date[:4]) * 365) + (int(i.date[5:7]) * 30) + (int(i.date[8:10]))) >= 10:
            i.status = 'بسته شده'
            i.save(using='profile')
    context = {'parts': parts, 'tickets': tickets, 'myuser': myuser}
    if request.method == 'POST':
        # send ticket
        subject = request.POST.get('subject')
        part = request.POST.get('part')
        text = request.POST.get('text')
        part_name = Group.objects.get(pk=part)
        ticket = Tickets(subject=subject, text=text, manager=part_name.name, manager_id=part,
                         user=request.user.username, user_id=request.user.pk, status='درحال بررسی',
                         user_ip=get_client_ip(request)[0])
        ticket.save(using='profile')
        ticket.ticket_id = ticket.pk + 100000  # The ticket number starts from one hundred
        ticket.save(using='profile')
        return redirect('profile_tickets')
    return render(request, 'front/Profile/profile_tickets.html', context=context)


@login_required
def profile_tickets_detail(request, pk):
    # for show details tickets
    if not request.user.is_active:  # Account activation notification
        messages.warning(request, 'Please activate your account')
        return redirect('profile_dashboard')
    myuser = CustomUser.objects.get(pk=request.user.pk)
    ticket = Tickets.objects.using('profile').get(pk=pk, user_id=request.user.pk)
    answertickets = AnswerTicket.objects.using('profile').order_by('-date').filter(ticket=ticket)
    context = {'ticket': ticket, 'answertickets': answertickets, 'number': len(answertickets), 'myuser': myuser}
    if request.method == 'POST':
        # User's response to admin's response
        text = request.POST.get('text')
        type_user = request.POST.get('type_user')
        answerticket = AnswerTicket(ticket=ticket, user=request.user.username, text=text, user_id=request.user.pk,
                                    type_user=type_user)
        answerticket.save(using='profile')
        return redirect('profile_detail_tickets', pk=pk)
    return render(request, 'front/Profile/profile_detail_tickets.html', context=context)


@login_required
def profile_orders(request):
    # for View orders
    carts = Cart.objects.filter(user_id=request.user.pk, user=request.user)
    myuser = CustomUser.objects.get(pk=request.user.pk)
    context = {'myuser': myuser, 'carts': carts}
    return render(request, 'front/Profile/profile_orders.html', context=context)


@login_required
def profile_details_order(request, order_code):
    # for show details order
    cart = Cart.objects.get(order_code=order_code)
    products_order_carts = ProductCart.objects.filter(cart_id=cart.pk)
    products_order_carts = Product.objects.filter(pk__in=products_order_carts.values('product_id'))
    products_order_address = Address.objects.get(pk=cart.address_id)
    myuser = CustomUser.objects.get(pk=request.user.pk)
    context = {'myuser': myuser, 'cart': cart, 'products_order_carts': products_order_carts,
               'products_order_address': products_order_address}
    return render(request, 'front/Profile/profile_details_order.html', context=context)


@login_required
def profile_my_favorite(request):
    # for show details favorites
    my_favorites = FavoriteProduct.objects.using('shop').filter(user_id=request.user.pk, user=request.user)[:4]
    my_favorites = Product.objects.filter(pk__in=my_favorites.values('product_id'))
    myuser = CustomUser.objects.get(pk=request.user.pk)
    context = {'myuser': myuser, 'my_favorites': my_favorites}
    return render(request, 'front/Profile/profile_my_favorite.html', context=context)


@login_required
def profile_delete_my_favorite(request, pk):
    # for delete my favorites
    if request.method == 'POST':
        my_favorites = FavoriteProduct.objects.using('shop').get(user_id=request.user.pk, user=request.user,
                                                                 product_id=pk)
        my_favorites.delete(using='shop')
        return redirect('profile_dashboard')

@login_required
def profile_change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')
        my_user=authenticate(username=request.user.username,password=old_password)
        if my_user is None:
            messages.error(request, 'لطفا رمز عبور صحیح را وارد کنید!')
            return redirect('profile_change_password')
        if new_password2 == new_password:
            messages.success(request,'رمز عبور با موفقیت تغییر کرد!')
            # my_user=CustomUser.objects.get(pk=request.user.pk)
            my_user.set_password(new_password)
            my_user.save()
        return redirect('profile_dashboard')
    return render(request, 'front/Profile/profile_change_password.html',)
