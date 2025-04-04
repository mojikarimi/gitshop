from __future__ import unicode_literals
from django.core.signing import Signer
from django.shortcuts import render, redirect
from django.http import JsonResponse
from ipware import get_client_ip

from Main.models import FAQCategory
from Profile.models import Address
from .models import Group, SubCategory, Category, Product, CommentsProduct, Cart, ProductCart, FavoriteProduct, \
    Question, StarProduct
from jdatetime import datetime
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from statistics import mean


def single_product(request, title):
    # Function to display a product
    product = Product.objects.using('shop').get(slug_name_product=title)  # Getting the product from the Shop database
    product.view += 1  # Increased product visit
    product.save(using='shop')
    questions = Question.objects.using('shop').filter(product_id=product.pk).order_by('-date')  # for questions user
    context = {'product': product, 'colors': eval(product.color), 'sizes': eval(product.size),
               'attrs': dict(zip(eval(product.attribute_title), eval(product.attribute_value))),
               # Send related features of each other
               'texts': zip(eval(product.title_text), eval(product.full_text)),  # Send text and Title together
               'questions': questions}
    my_star = StarProduct.objects.filter(user=request.user.username, product_id=product.pk,
                                         user_ip=get_client_ip(request)[0])  # for star
    if my_star:
        # for star rating
        context['my_star'] = my_star[0]
    product_comments = CommentsProduct.objects.using('shop').filter(pk_product=product.pk, confirmed=True)

    if product_comments:
        # Show user comments
        build = mean(
            list(product_comments.values_list('build', flat=True))) * 20  # Average characteristics in percentage
        innovation = mean(
            list(product_comments.values_list('innovation', flat=True))) * 20  # Average characteristics in percentage
        ease_of_use = mean(
            list(product_comments.values_list('ease_of_use', flat=True))) * 20  # Average characteristics in percentage
        designing = mean(
            list(product_comments.values_list('designing', flat=True))) * 20  # Average characteristics in percentage
        possibilities = mean(list(
            product_comments.values_list('possibilities', flat=True))) * 20  # Average characteristics in percentage
        worth_buying = mean(
            list(product_comments.values_list('worth_buying', flat=True))) * 20  # Average characteristics in percentage
        context['build'] = build
        context['innovation'] = innovation
        context['ease_of_use'] = ease_of_use
        context['designing'] = designing
        context['possibilities'] = possibilities
        context['worth_buying'] = worth_buying
        context['product_comments'] = product_comments
        context['product_comments_weaknesses'] = [(x.pk, eval(x.weaknesses)) for x in
                                                  product_comments]  # To show weaknesses
        context['product_comments_strengths'] = [(x.pk, eval(x.strengths)) for x in
                                                 product_comments]  # To show strengths
        context['len_product_comments'] = len(product_comments)  # for show len comments in template
    if 'product_view' in request.session:
        # To add a product to recent visits
        product_view = request.session.get('product_view')
        request.session.delete('product_view')
        product_view.append(title)
        request.session['product_view'] = list(set(product_view))
        # There was an error that sent only one product, so I changed it this way
    elif 'product_view' not in request.session:
        request.session['product_view'] = [title]
    if len(FavoriteProduct.objects.filter(user_id=request.user.pk, user=request.user,
                                          product_id=product.pk)):  # It is used to show liking
        context['my_favorite'] = FavoriteProduct.objects.filter(user_id=request.user.pk, user=request.user,
                                                                product_id=product.pk).first()
    else:
        context['my_favorite'] = None

    return render(request, 'front/Shop/single_product.html', context=context)


def star_product(request):
    # To rate products
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        value = request.POST.get('value')
        my_star, _ = StarProduct.objects.get_or_create(product_id=product_id, user=request.user.username,
                                                       user_ip=get_client_ip(request)[0])
        product = Product.objects.get(pk=product_id)
        if _ == False:  # If the privilege was available
            # To get the sum of numbers by subtracting the previous score
            sum_star = (float(value) - float(my_star.star)) + (product.star * product.star_number)
            product.star = sum_star / product.star_number
            product.save(using='shop')
        else:  # If the privilege is not available
            # To get the sum of numbers by subtracting the previous score
            sum_star = (float(value) - float(my_star.star)) + (product.star * product.star_number)
            product.star_number += 1
            product.star = sum_star / product.star_number
            product.save(using='shop')
        my_star.star = value
        my_star.save(using='shop')
        return JsonResponse({})


@login_required
def my_favorite_product(request):
    # To add a product to Favorites
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        status = request.POST.get('status')
        my_favorite = FavoriteProduct.objects.filter(user_id=request.user.pk, user=request.user, product_id=product_id)
        if len(my_favorite) >= 1:  # If a product is available, continue the bet
            my_favorite.delete()

        else:
            # Create a new model to add to favorites
            my_fav = FavoriteProduct(user_id=request.user.pk, user=request.user, product_id=product_id, status=status)
            my_fav.save(using='shop')
        return JsonResponse({})


def products(request):
    # Product display function
    products_views = Product.objects.using('shop').order_by('-view')  # Based on the number of visits
    products_news = Product.objects.using('shop').order_by('-date')  # new products
    products_sales = Product.objects.using('shop').order_by('-sales_number')  # Based on the sale of products
    products_expensives = Product.objects.using('shop').order_by('price')  # Based on the price of products (expensive)
    products_inexpensives = Product.objects.using('shop').order_by(
        '-price')  # Based on the price of products(inexpensive)
    colors = list(set([s for product in Product.objects.all() for s in eval(product.color)]))  # get colors
    context = {'products_news': products_news, 'products_views': products_views, 'products_sales': products_sales,
               'products_expensives': products_expensives, 'products_inexpensives': products_inexpensives,
               'colors': colors}
    return render(request, 'front/Shop/products.html', context=context)


def products_searchs(request):
    # Search with search box
    if request.method == 'POST':
        search = request.POST.get('search')
        products_searchs = Product.objects.filter(
            Q(name_product__icontains=search) | Q(description__icontains=search))  # Taking queries
        colors = list(set([s for product in Product.objects.all() for s in eval(product.color)]))  # get colors
        return render(request, 'front/Shop/products_searchs.html',
                      {'products_searchs': products_searchs, 'search': search, 'colors': colors})


def product_group_category_subcategory(request, title):
    # for search with Group , Category , Sub Category
    products_search = Product.objects.filter(Q(category=title) | Q(group=title) | Q(sub_category=title))
    colors = list(set([s for product in Product.objects.all() for s in eval(product.color)]))  # get colors
    return render(request, 'front/Shop/products_searchs.html',
                  {'products_searchs': products_search, 'colors': colors})


def products_order(request, order):
    # for See the best selling products
    products_search = Product.objects.order_by(order)
    colors = list(set([s for product in Product.objects.all() for s in eval(product.color)]))  # get colors
    return render(request, 'front/Shop/products_searchs.html',
                  {'products_searchs': products_search, 'colors': colors})


def search_filter(request):
    # Search with search box
    if request.method == 'POST':
        group_filter = request.POST.getlist('group_filter')
        category_filter = request.POST.getlist('category_filter')
        subcategory_filter = request.POST.getlist('subcategory_filter')
        color_filter = request.POST.getlist('color_filter')
        color_filter = str(color_filter).replace(', ', '|')[1:-1]
        # [1:-1]=> color_filter =['#ddcsds','#ccxddf','#dkwdds'] -> '#ddcsds','#ccxddf','#dkwdds'
        if not color_filter:
            color_filter = '/'  # To prevent the regex from crashing
        products_searchs = Product.objects.filter(
            Q(group__in=group_filter) | Q(category__in=category_filter) | Q(sub_category__in=subcategory_filter) | Q(
                color__regex=color_filter))  # get queries
        colors = list(set([s for product in Product.objects.all() for s in eval(product.color)]))  # get colors
        return render(request, 'front/Shop/products_searchs.html',
                      {'products_searchs': products_searchs, 'colors': colors})


@login_required
def product_comments(request, title):
    # It is used to make product comments
    product = Product.objects.using('shop').get(name_product=title)  # It takes the desired product
    context = {'product': product}
    if request.method == 'POST':
        # Get form values
        build = request.POST.get('build')
        innovation = request.POST.get('innovation')
        ease_of_use = request.POST.get('ease_of_use')
        designing = request.POST.get('designing')
        possibilities = request.POST.get('possibilities')
        worth_buying = request.POST.get('worth_buying')
        title = request.POST.get('title')
        strengths = request.POST.getlist('strengths')
        weaknesses = request.POST.getlist('weaknesses')
        text = request.POST.get('text')
        tender = request.POST.get('tender')
        # Make a comment
        product_comment = CommentsProduct(pk_product=product.pk, user_id=request.user.pk, user=request.user.username,
                                          innovation=innovation, build=build,
                                          ease_of_use=ease_of_use, designing=designing, possibilities=possibilities,
                                          worth_buying=worth_buying, title=title, strengths=strengths,
                                          weaknesses=weaknesses, text=text, tender=tender)
        product_comment.save(using='shop')
        return redirect('single_product', title=product.slug_name_product)
    return render(request, 'front/Shop/product_comments.html', context=context)


@login_required
def cart(request):
    # Add product to cart
    if request.method == 'POST':
        # Getting data from the form
        product_id = request.POST.get('product_id')
        product = Product.objects.get(pk=product_id)
        size = request.POST.get('size')
        color = request.POST.get('color')
        # Taking a shopping cart that has not yet been confirmed and the payment process has not been completed
        carts = Cart.objects.using('shop').filter(user_id=request.user.pk, status=False)
        if len(carts) >= 1:
            # If it is in the shopping cart, it will be added to it
            carts = carts.first()
            if not ProductCart.objects.filter(cart_id=carts.pk, product_id=product_id, size=size, color=color).exists():
                # If the exact same product is not in the shopping cart, it will be added
                product_cart = ProductCart(cart_id=carts.pk, product_id=product_id, size=size, color=color)
                # The total price has not increased in the shopping cart
                carts.price += product.discounted_price
                carts.save(using='shop')
                product_cart.save(using='shop')
                product.order_number += 1
                # It increases the number of orders by one so that it does not exceed the capacity limit
                product.save(using='shop')
        else:
            # If there was no shopping cart, it would make one
            sign = Signer(key='eww@z3os_-1!fu&j-ic&%adl%428ztm8v6)7ey72aw$mt64!1(')
            new_cart = Cart(user_id=request.user.pk, user=request.user, price=product.discounted_price)
            new_cart.save(using='shop')
            product_cart = ProductCart(cart_id=new_cart.pk, product_id=product_id, size=size, color=color)
            product_cart.save(using='shop')
            product.order_number += 1
            product.save(using='shop')
            # set an order code for cart
            cart_order_code = Cart.objects.using('shop').get(user_id=request.user.pk, user=request.user, status=False)
            cart_order_code.order_code = str(sign.sign_object(cart_order_code.id + 100000 + request.user.pk))[8:28]
            cart_order_code.save(using='shop')

        return redirect(request.META['HTTP_REFERER'])
    return render(request, 'front/Shop/cart.html')


def delete_product_from_cart(request):
    # for delete a product from cart
    if request.method == 'POST':
        product_cart_pk = request.POST.get('product_cart_pk')
        product_cart = ProductCart.objects.get(pk=product_cart_pk)
        cart = Cart.objects.get(pk=product_cart.cart_id)
        # Reducing the price of items removed from the shopping cart
        cart.price -= (product_cart.number * Product.objects.get(pk=product_cart.product_id).discounted_price)
        cart.save(using='shop')
        product_cart.delete(using='shop')
        return redirect('cart')


@login_required
def cart_number_plus(request):
    # To increase the number of products ordered
    if request.method == 'POST':
        # A shopping cart whose purchase process has not yet been completed
        carts = Cart.objects.using('shop').filter(user_id=request.user.pk, status=False).first()
        cart_product_pk = request.POST['product_id'][8:]
        cart_product = ProductCart.objects.get(pk=cart_product_pk)
        product = Product.objects.get(pk=cart_product.product_id)
        if (product.number > cart_product.number) and (product.order_number != product.number):
            # Check the order number with the existing number
            cart_product.number += 1
            # Increase the number of products
            cart_product.save(using='shop')
            # Increase the total price in the shopping cart
            carts.price += product.discounted_price
            # Increase the number ordered in the product model
            product.order_number += 1
            product.save(using='shop')
            carts.save(using='shop')
            return JsonResponse({})


@login_required
def cart_number_minus(request):
    # Reduce the number of products ordered
    if request.method == 'POST':
        # A shopping cart whose purchase process has not yet been completed
        carts = Cart.objects.using('shop').filter(user_id=request.user.pk, status=False).first()
        cart_product_pk = request.POST['product_id'][8:]
        cart_product = ProductCart.objects.get(pk=cart_product_pk)
        product = Product.objects.get(pk=cart_product.product_id)
        if (cart_product.number > 1) and (product.order_number > 0):
            # The number in the shopping cart should be more than one and the number of orders should be more than zero
            cart_product.number -= 1
            # Reduce the number of products
            cart_product.save(using='shop')
            # Reduction of the total price in the shopping cart
            carts.price -= product.discounted_price
            # Reduce the number of orders in the product model
            product.order_number -= 1
            product.save(using='shop')
            carts.save(using='shop')
            return JsonResponse({})


@login_required
def shopping(request):
    # Determining the address and delivery method
    addresses = Address.objects.filter(user=request.user, user_id=request.user.pk)
    if request.method == 'POST':
        # Change the selected address
        address = request.POST.get('address')
        x = addresses.get(pk=address)
        addresses.update(status=False)
        x.status = 1
        x.save(using='profile')
        return redirect('shopping')
    context = {'addresses': addresses}
    if addresses:
        active_address = addresses.get(status=1)
        context['active_address'] = active_address

    return render(request, 'front/Shop/shopping.html', context=context)


@login_required
def shopping_peyment(request):
    # Address registration and shipping method(sending_method,address,...)
    if request.method == 'POST':
        sending_method = request.POST.get('sending_method')
        address = request.POST.get('address')
        carts = Cart.objects.get(user_id=request.user.pk, user=request.user, status=False)
        carts.sending_method = sending_method
        carts.address_id = address
        carts.save(using='shop')
        return render(request, 'front/Shop/shopping_peyment.html')


@login_required
def shopping_complete_buy(request):
    # The last step is to complete the shopping cart
    if request.method == 'POST':

        try:
            carts = Cart.objects.get(user_id=request.user.pk, user=request.user, status=False)
            product_sales = ProductCart.objects.filter(cart_id=carts.pk)
            product = Product.objects.filter(pk__in=product_sales.values_list('product_id', flat=True))
            for i in product_sales:
                f = product.get(pk=i.product_id)
                f.sales_number += i.number
                f.number -= i.number
                f.save(using='shop')
        except:
            return redirect('index')
        carts.status = True  # change status cart to True
        carts.save(using='shop')
        address = Address.objects.get(pk=carts.address_id)
        number = len(ProductCart.objects.filter(cart_id=carts.pk))
        context = {'cart': carts, 'number': number, 'address': address}
        return render(request, 'front/Shop/shopping_complete_buy.html', context=context)


def add_questions(request):
    # User questions about a product
    if request.method == 'POST':
        text = request.POST.get('text')
        product_id = request.POST.get('product_id')
        product = Product.objects.get(pk=product_id)
        question = Question(product_id=product.pk, user_id=request.user.pk, user=request.user, text=text)
        question.save(using='shop')

        return redirect('single_product', product.name_product)


#########################################  Panel  #################################################################
# Create your views here.
@login_required
@permission_required(perm='Shop.add_group')
def panel_add_group_product(request):
    # for add group product
    if not request.user.is_staff:
        return redirect('index')
    groups = Group.objects.using('shop').all()
    if request.method == 'POST':
        group = request.POST.get('group')
        if len(groups.filter(name=group)) >= 1:  # Calculation of the number of categories with this title
            # messages.error(request, 'There is a category with this title')
            return redirect('panel_add_group_product')

        image = request.FILES.get('image')
        if image:
            if str(image.content_type).startswith('image'):
                if image.size <= 5242880:  # The size of the photo must be less than 5 MB
                    Group.objects.create(image=image, name=group)
                    messages.success(request, 'Successfully added')
                    return redirect('panel_add_group_product')
                else:
                    messages.error(request, 'More volume than the permissible limit')
                    return redirect('panel_add_group_product')
            else:
                messages.error(request, 'The photo format is incorrect')
                return redirect('panel_add_group_product')
        else:
            messages.error(request, 'The photo is not available')
            return redirect('panel_add_group_product')

    context = {'groups': groups}
    return render(request, 'back/PanelShop/add_group_product.html', context=context)


@login_required
@permission_required(perm='Shop.change_group')
def panel_edit_group_product(request, pk):
    # for edit group product
    if not request.user.is_staff:
        return redirect('index')

    if request.method == 'POST':
        group_new = request.POST.get('group_new')
        if len(Group.objects.using('shop').filter(~Q(pk=pk),
                                                  name=group_new)) >= 1:  # Calculation of the number of categories with this title
            # messages.error(request, 'There is a category with this title')
            return redirect('panel_add_group_product')
        group_edit = Group.objects.using('shop').get(pk=pk)
        # edit image group
        image = request.FILES.get('new_image')
        if image:  # update image
            if str(image.content_type).startswith('image'):
                if image.size <= 5242880:
                    group_edit.image = image
                else:
                    messages.warning(request, 'More volume than the permissible limit')
                    return redirect('panel_add_group_product')
            else:
                messages.warning(request, 'The photo format is incorrect')
                return redirect('panel_add_group_product')
        group_edit.name = group_new
        group_edit.save(using='shop')
        messages.success(request, 'Successfully edited')
        return redirect('panel_add_group_product')


@login_required
@permission_required(perm='Shop.delete_group')
def panel_delete_group_product(request, pk):
    # for delete group product
    if not request.user.is_staff:
        return redirect('index')
    Group.objects.using('shop').get(pk=pk).delete()
    return redirect('panel_add_group_product')


@login_required
@permission_required(perm='Shop.add_category')
def panel_add_category_product(request):
    # for add category product
    if not request.user.is_staff:
        return redirect('index')

    groups = Group.objects.using('shop').all()
    categories = Category.objects.using('shop').all()
    if request.method == 'POST':
        group = request.POST.get('group')
        group_id = groups.get(name=group).pk
        category = request.POST.get('category')
        if len(categories.filter(name=category,
                                 group=group)) >= 1:  # Calculation of the number of categories with this title
            # messages.error(request, 'There is a category with this title')
            return redirect('panel_add_category_product')
        new_category = Category(name=category, group_id=group_id, group=group)
        new_category.save(using='shop')
    context = {'groups': groups, 'categories': categories}
    return render(request, 'back/PanelShop/add_category_product.html', context=context)


@login_required
@permission_required(perm='Shop.delete_category')
def panel_delete_category_product(request, pk):
    # for delete category product
    if not request.user.is_staff:
        return redirect('index')
    Category.objects.using('shop').get(pk=pk).delete()
    return redirect('panel_add_category_product')


@login_required
@permission_required(perm='Shop.change_category')
def panel_edit_category_product(request, pk):
    # for edit category product
    if not request.user.is_staff:
        return redirect('index')

    if request.method == 'POST':
        group_new = request.POST.get('group_new')
        group_id = Group.objects.get(name=group_new).pk
        category_new = request.POST.get('category_new')
        if len(Category.objects.using('shop').filter(name=category_new,
                                                     group=group_new)) >= 1:  # Calculation of the number of categories with this title
            # messages.error(request, 'There is a category with this title')
            return redirect('panel_add_category_product')
        category_edit = Category.objects.using('shop').get(pk=pk)
        category_edit.group = group_new
        category_edit.group_id = group_id
        category_edit.name = category_new
        category_edit.save(using='shop')
        return redirect('panel_add_category_product')


@login_required
@permission_required(perm='Shop.add_subcategory')
def panel_add_subcategory_product(request):
    # for add new sub category
    if not request.user.is_staff:
        return redirect('index')
    groups = Group.objects.using('shop').all()
    categories = Category.objects.using('shop').all()
    subcategories = SubCategory.objects.using('shop').all()
    if request.method == 'POST':
        group = request.POST.get('group')
        group_id = groups.get(name=group).pk
        category = request.POST.get('category')
        category_id = categories.get(name=category).pk
        subcategory = request.POST.get('subcategory')
        if len(subcategories.using('shop').filter(name=subcategory, category=category,
                                                  group=group)) >= 1:  # Calculation of the number of categories with this title
            # messages.error(request, 'There is a category with this title')
            return redirect('panel_add_subcategory_product')
        new_subcategory = SubCategory(name=subcategory, group_id=group_id, group=group, category_id=category_id,
                                      category=category)
        new_subcategory.save(using='shop')
    context = {'groups': groups, 'categories': categories, 'subcategories': subcategories}
    return render(request, 'back/PanelShop/add_subcategory_product.html', context=context)


@login_required
@permission_required(perm='Shop.delete_subcategory')
def panel_delete_subcategory_product(request, pk):
    # for delete sub category product
    if not request.user.is_staff:
        return redirect('index')
    SubCategory.objects.using('shop').get(pk=pk).delete()
    return redirect('panel_add_subcategory_product')


@login_required
@permission_required(perm='Shop.add_product')
def panel_add_product(request):
    # for add product
    if not request.user.is_staff:
        return redirect('index')
    groups = Group.objects.using('shop').all()  # get gruops
    categories = Category.objects.using('shop').all()  # get categories
    subcategories = SubCategory.objects.using('shop').all()  # get sub categories
    if request.method == 'POST':
        title = request.POST.get('title')
        title_english = request.POST.get('title_english')
        group = request.POST.get('group')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        GCS = subcategories.using('shop').filter(category=category, group=group,
                                                 name=subcategory)  # G=group C=category S=subcategory
        if len(GCS) == 0:  # match  G=group, C=category, S=subcategory
            messages.error(request, 'not macht category & group & subcategory!! ')
            return redirect('panel_add_product')
        # get images
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')
        # get video
        video = request.FILES.get('video')
        # get another details
        number = request.POST.get('number')
        price = request.POST.get('price')
        percent = request.POST.get('percent')
        to_day = request.POST.get('to_day')
        description = request.POST.get('description')
        title_text = request.POST.getlist('title_text')
        full_text = request.POST.getlist('full_text')
        color = request.POST.getlist('color')
        size = request.POST.getlist('size')
        input_title = request.POST.getlist('input_title')
        input_value = request.POST.getlist('input_value')
        amazing_offer = request.POST.get('amazing_offer')
        our_suggestion = request.POST.get('our_suggestion')
        instant_sale = request.POST.get('instant_sale')
        available = request.POST.get('available')
        # set time for product
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        if len(str(month)) == 1:
            month = '0' + str(month)
        if len(str(day)) == 1:
            day = '0' + str(day)
        if amazing_offer == 'on':
            amazing_offer = True
        else:
            amazing_offer = False
        if our_suggestion == 'on':
            our_suggestion = True
        else:
            our_suggestion = False
        if available == 'on':
            available = True
        else:
            available = False
        if instant_sale == 'on':
            instant_sale = True
        else:
            instant_sale = False
        # add new product
        Product.objects.using('shop').create(description=description, name_product=title,
                                             name_product_english=title_english, group=GCS[0].group,
                                             group_id=GCS[0].group_id, category=GCS[0].category,
                                             category_id=GCS[0].category_id,
                                             sub_category=subcategory, sub_category_id=GCS[0].pk, color=color,
                                             size=size,
                                             image1=image1, image2=image2, image3=image3, image4=image4, video=video,
                                             attribute_title=input_title, attribute_value=input_value, price=price,
                                             discount_percent=int(float(percent)), number=number,
                                             discount_period=to_day,
                                             discounted_price=int(
                                                 float(price) - (float(price) * (float(percent) / 100))),
                                             instant_sale=instant_sale,
                                             available=available, amazing_offer=amazing_offer,
                                             our_suggestion=our_suggestion,
                                             full_text=full_text, title_text=title_text, date=f'{year}/{month}/{day}')
        return redirect('panel_add_product')
    context = {
        'groups': groups,
        'subcategories': subcategories,
        'categories': categories,
    }
    return render(request, 'back/PanelShop/add_product.html', context=context)


@login_required
@permission_required(perm='Shop.change_product')
def panel_edit_product(request, pk):
    # for edit details a product
    if not request.user.is_staff:
        return redirect('index')
    product = Product.objects.using('shop').get(pk=pk)  # get product
    groups = Group.objects.using('shop').all()  # get groups
    categories = Category.objects.using('shop').all()  # get categories
    subcategories = SubCategory.objects.using('shop').all()  # get sub categories
    if request.method == 'POST':
        subcategories = SubCategory.objects.using('shop').all()
        title = request.POST.get('new_title')
        title_english = request.POST.get('new_title_english')
        group = request.POST.get('new_group')
        category = request.POST.get('new_category')
        subcategory = request.POST.get('new_subcategory')
        GCS = subcategories.filter(category=category, group=group, name=subcategory)  # G=group C=category S=subcategory
        if len(GCS) == 0:  # match category, group, subcategory
            return redirect('panel_add_product')
        # get image product
        image1 = request.FILES.get('new_image1')
        image2 = request.FILES.get('new_image2')
        image3 = request.FILES.get('new_image3')
        image4 = request.FILES.get('new_image4')
        # get video product
        video = request.FILES.get('new_video')
        # get another details for update
        number = request.POST.get('new_number')
        price = request.POST.get('new_price')
        percent = request.POST.get('new_percent')
        to_day = request.POST.get('new_to_day')
        description = request.POST.get('description')
        title_text = request.POST.getlist('new_title_text')
        full_text = request.POST.getlist('new_full_text')
        color = request.POST.getlist('new_color')
        size = request.POST.getlist('new_size')
        input_title = request.POST.getlist('new_input_title')
        input_value = request.POST.getlist('new_input_value')
        amazing_offer = request.POST.get('new_amazing_offer')
        our_suggestion = request.POST.get('new_our_suggestion')
        instant_sale = request.POST.get('new_instant_sale')
        available = request.POST.get('new_available')
        if amazing_offer == 'on':
            amazing_offer = True
        else:
            amazing_offer = False
        if our_suggestion == 'on':
            our_suggestion = True
        else:
            our_suggestion = False
        if available == 'on':
            available = True
        else:
            available = False
        if instant_sale == 'on':
            instant_sale = True
        else:
            instant_sale = False
        edit_product = Product.objects.using('shop').get(pk=pk)
        edit_product.instant_sale = instant_sale
        edit_product.available = available
        edit_product.our_suggestion = our_suggestion
        edit_product.amazing_offer = amazing_offer
        edit_product.full_text = full_text
        edit_product.description = description
        edit_product.title_text = title_text
        edit_product.attribute_title = input_title
        edit_product.attribute_value = input_value
        edit_product.color = color
        edit_product.size = size
        edit_product.price = price
        edit_product.number = number
        edit_product.discount_period = to_day
        edit_product.discounted_price = int(float(price) - (float(price) * (float(percent) / 100)))
        edit_product.discount_percent = int(float(percent))
        edit_product.name_product_english = title_english
        edit_product.name_product = title
        edit_product.group = GCS[0].group
        edit_product.group_id = GCS[0].group_id
        edit_product.category = GCS[0].category
        edit_product.category_id = GCS[0].category_id
        edit_product.sub_category = GCS[0].name
        edit_product.sub_category_id = GCS[0].pk
        # If there is a photo or video, it will be changed

        # If there is a photo or video, it will be changed
        if image1:
            edit_product.image1 = image1
        if image2:
            edit_product.image2 = image2
        if image3:
            edit_product.image3 = image3
        if image4:
            edit_product.image4 = image4
        if video:
            edit_product.video = video

        edit_product.save(using='shop')
        return redirect('panel_list_product')
    title_text = eval(product.title_text)  # eval('[1,2,3]')=> [1,2,3]-> List not STR
    full_text = eval(product.full_text)
    colors = eval(product.color)
    sizes = eval(product.size)
    attr_title = eval(product.attribute_title)
    attr_value = eval(product.attribute_value)
    context = {
        'product': product,
        'groups': groups,
        'subcategories': subcategories,
        'categories': categories,
        'colors': colors,
        'sizes': sizes,
        'attrs': zip(attr_title, attr_value),
        'text': zip(title_text, full_text),

    }
    return render(request, 'back/PanelShop/edit_product.html', context=context)


@login_required
@permission_required(perm='Shop.view_product')
def panel_list_product(request):
    # see list product
    if not request.user.is_staff:
        return redirect('index')
    panel_list_products = Product.objects.using('shop').order_by('-date')
    context = {'panel_list_products': panel_list_products}
    return render(request, 'back/PanelShop/list_product.html', context=context)


@login_required
@permission_required(perm='Shop.view_commentsproduct')
def panel_comments_product(request, pk_product):
    # see comments product list
    panel_comments = CommentsProduct.objects.filter(pk_product=pk_product)
    product_comment = Product.objects.get(pk=pk_product)
    return render(request, 'back/PanelShop/comments_product.html',
                  {'panel_comments': panel_comments, 'product_comment': product_comment})


@login_required
@permission_required(perm='Shop.view_commentsproduct')
def panel_details_comments(request, pk_comment):
    # see details comment product
    panel_comment = CommentsProduct.objects.using('shop').get(pk=pk_comment)
    if request.method == 'POST':
        confirmed = request.POST.get('confirmed')
        if confirmed:  # update status
            confirmed = True
        else:
            confirmed = False
        panel_comment.confirmed = confirmed
        panel_comment.save(using='shop')
        return redirect('panel_details_comments', pk_comment)
    return render(request, 'back/PanelShop/details_comment.html', {'panel_comment': panel_comment})


@login_required
@permission_required(perm='Shop.delete_commentsproduct')
def panel_delete_comment(request, pk_comment):
    # for delete comment product with pk
    delete_comment = CommentsProduct.objects.using('shop').get(pk=pk_comment)
    pk_product = delete_comment.pk_product
    delete_comment.delete(using='shop')
    return redirect('panel_comments_product', pk_product)


@login_required
@permission_required(perm='Shop.delete_product')
def panel_delete_product(request, pk):
    # for delete a product
    if not request.user.is_staff:
        return redirect('index')
    product = Product.objects.using('shop').get(pk=pk)
    product.delete(using='shop')
    return redirect('panel_list_product')


@login_required
@permission_required(perm='Shop.change_subcategory')
def panel_edit_subcategory_product(request, pk):
    # for edit sub category product
    if not request.user.is_staff:
        return redirect('index')
    if request.method == 'POST':
        group_new = request.POST.get('group_new')
        group_id = Group.objects.using('shop').get(name=group_new).pk
        category_new = request.POST.get('category_new')
        category_id = Category.objects.using('shop').get(name=category_new).pk
        subcategory_new = request.POST.get('subcategory_new')
        if len(SubCategory.objects.using('shop').filter(
                name=subcategory_new, category=category_new,
                group=group_new)) >= 1:  # Calculation of the number of categories with this title
            # messages.error(request, 'There is a category with this title')
            return redirect('panel_add_subcategory_product')
        subcategory_edit = SubCategory.objects.using('shop').get(pk=pk)
        subcategory_edit.group = group_new
        subcategory_edit.group_id = group_id
        subcategory_edit.category = category_new
        subcategory_edit.category_id = category_id
        subcategory_edit.name = subcategory_new
        subcategory_edit.save(using='shop')
        return redirect('panel_add_subcategory_product')


@login_required
@permission_required(perm='Shop.view_cart')
def panel_view_cart(request):
    # see shopping carts
    panel_carts = Cart.objects.order_by('-date')
    context = {'panel_carts': panel_carts}
    return render(request, 'back/PanelShop/list_cart.html', context=context)


@login_required
@permission_required(perm='Shop.view_cart')
def panel_details_cart(request, pk):
    # see details shoppin cart
    panel_cart = Cart.objects.get(pk=pk)
    panel_products_cart = ProductCart.objects.filter(cart_id=panel_cart.pk).order_by('product_id')
    panel_products = Product.objects.filter(pk__in=panel_products_cart.values('product_id'))
    panel_address = Address.objects.get(pk=panel_cart.address_id)
    context = {'panel_cart': panel_cart, 'panel_products_cart': panel_products_cart, 'panel_products': panel_products,
               'panel_address': panel_address}
    if request.method == 'POST':
        # Updating product delivery procedures
        preparation = request.POST.get('preparation')
        exit_ = request.POST.get('exit')
        delivery = request.POST.get('delivery')
        exchange = request.POST.get('exchange')
        customer = request.POST.get('customer')

        if preparation:
            preparation = True
        else:
            preparation = False
        if exit_:
            exit_ = True
        else:
            exit_ = False
        if delivery:
            delivery = True
        else:
            delivery = False
        if exchange:
            exchange = True
        else:
            exchange = False
        if customer:
            customer = True
        else:
            customer = False
        panel_cart.preparation = preparation
        panel_cart.exit = exit_
        panel_cart.delivery = delivery
        panel_cart.exchange = exchange
        panel_cart.customer = customer
        panel_cart.save(using='shop')
        return redirect('panel_details_cart', pk=pk)
    return render(request, 'back/PanelShop/details_cart.html', context=context)


@login_required
@permission_required(perm='Shop.view_question')
def panel_questions_list(request, pk):
    # see questions list
    questions = Question.objects.using('shop').filter(product_id=pk).order_by('sort')
    return render(request, 'back/PanelShop/questions_list.html', {'questions': questions, 'pk_faq': pk})


@login_required
@permission_required(perm='Shop.change_question')
def panel_sort_question(request, pk):
    # for sort questions
    if request.method == 'POST':
        questions = Question.objects.all()
        sorts = request.POST.getlist('sort')
        for i, x in enumerate(sorts):  # [5,4,6] => 0->5, 1->4, 2->6
            question = questions.get(pk=x)
            question.sort = i + 1
            question.save(using='shop')
        return redirect('panel_questions_list', pk=pk)


@login_required
@permission_required(perm='Shop.change_question')
def panel_details_question(request, pk):
    # See the details of the questions end edit(status, FAQ)
    question = Question.objects.get(pk=pk)
    faq_categories = FAQCategory.objects.all()
    if request.method == 'POST':
        answer_text = request.POST.get('answer_text')
        faq = request.POST.get('faq')
        status = request.POST.get('status')
        faq_category = request.POST.get('faq_category')
        if faq:
            faq = True
        else:
            faq = False
        if status:
            status = True
        else:
            status = False
        question.answer_text = answer_text  # Record the answer to the question
        question.faq = faq
        question.category = faq_category
        question.status = status
        if not question.answer_date:  # To record the time for the first time an answer is given
            question.answer_date = datetime.now()
        question.save(using='shop')
        return redirect('panel_details_question', pk)

    return render(request, 'back/PanelShop/details_questions.html',
                  {'question': question, 'faq_categories': faq_categories})


@login_required
@permission_required(perm='Shop.delete_question')
def panel_delete_question(request, pk):
    # for delete Question
    question = Question.objects.using('shop').get(pk=pk)
    pk_product = question.product_id
    question.delete(using='shop')
    return redirect('panel_questions_list', pk=pk_product)
