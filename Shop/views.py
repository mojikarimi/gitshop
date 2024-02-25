from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import Group, SubCategory, Category, Product, CommentsProduct, Cart, ProductCart
from jdatetime import datetime
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required


def single_product(request, title):
    # Function to display a product
    product = Product.objects.using('shop').get(name_product=title)  # Getting the product from the Shop database
    product.view += 1  # Increased product visit
    product.save(using='shop')
    context = {'product': product, 'colors': eval(product.color), 'sizes': eval(product.size),
               'attrs': dict(zip(eval(product.attribute_title), eval(product.attribute_value))),
               # Send related features of each other
               'texts': zip(eval(product.title_text), eval(product.full_text))}  # Send text and title Title together
    return render(request, 'front/Shop/single_product.html', context=context)


def products(request):
    # Product display function
    products_views = Product.objects.using('shop').order_by('-view')  # Based on the number of visits
    products_news = Product.objects.using('shop').order_by('-date')  # new products
    products_sales = Product.objects.using('shop').order_by('-sales_number')  # Based on the sale of products
    products_expensives = Product.objects.using('shop').order_by('price')  # Based on the price of products (expensive)
    products_inexpensives = Product.objects.using('shop').order_by(
        '-price')  # Based on the price of products(inexpensive)
    context = {'products_news': products_news, 'products_views': products_views, 'products_sales': products_sales,
               'products_expensives': products_expensives, 'products_inexpensives': products_inexpensives, }
    return render(request, 'front/Shop/products.html', context=context)


def search(request):
    return render(request, 'front/Shop/products.html')


def product_comments(request, title):
    product = Product.objects.using('shop').get(name_product=title)
    context = {'product': product}
    if request.method == 'POST':
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
        product_comment = CommentsProduct(pk_product=product.pk, user_id=request.user.pk, user=request.user.username,
                                          innovation=innovation, build=build,
                                          ease_of_use=ease_of_use, designing=designing, possibilities=possibilities,
                                          worth_buying=worth_buying, title=title, strengths=strengths,
                                          weaknesses=weaknesses, text=text, tender=tender)
        product_comment.save(using='shop')
        return redirect('single_product', title=product.name_product)
    return render(request, 'front/Shop/product_comments.html', context=context)


@login_required
def cart(request):
    if request.method == 'POST':

        product_id = request.POST.get('product_id')
        product=Product.objects.get(pk=product_id)
        size = request.POST.get('size')
        color = request.POST.get('color')
        carts = Cart.objects.using('shop').filter(user_id=request.user.pk, status=False).first()
        if carts:
            if not ProductCart.objects.filter(cart_id=carts.pk, product_id=product_id, size=size, color=color).exists():
                product_cart = ProductCart(cart_id=carts.pk, product_id=product_id, size=size, color=color)
                carts.price+= product.discounted_price
                carts.save(using='shop')
                product_cart.save(using='shop')
        else:
            new_cart = Cart(user_id=request.user.pk, user=request.user,price=product.discounted_price)
            new_cart.save(using='shop')
            product_cart = ProductCart(cart_id=new_cart.pk, product_id=product_id, size=size, color=color)
            product_cart.save(using='shop')

        return redirect(request.META['HTTP_REFERER'])


#########################################  Panel  #################################################################
# Create your views here.
@login_required
@permission_required(perm='Shop.add_group')
def panel_add_group_product(request):
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
                if image.size <= 5242880:
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
    if not request.user.is_staff:
        return redirect('index')

    if request.method == 'POST':
        group_new = request.POST.get('group_new')
        if len(Group.objects.using('shop').filter(~Q(pk=pk),
                                                  name=group_new)) >= 1:  # Calculation of the number of categories with this title
            # messages.error(request, 'There is a category with this title')
            return redirect('panel_add_group_product')
        group_edit = Group.objects.using('shop').get(pk=pk)
        image = request.FILES.get('new_image')
        if image:
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
    if not request.user.is_staff:
        return redirect('index')
    Group.objects.using('shop').get(pk=pk).delete()
    return redirect('panel_add_group_product')


@login_required
@permission_required(perm='Shop.add_category')
def panel_add_category_product(request):
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
    if not request.user.is_staff:
        return redirect('index')
    Category.objects.using('shop').get(pk=pk).delete()
    return redirect('panel_add_category_product')


@login_required
@permission_required(perm='Shop.change_category')
def panel_edit_category_product(request, pk):
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
        category_edit.group = category_new
        category_edit.group_id = group_id
        category_edit.name = category_new
        category_edit.save(using='shop')
        return redirect('panel_add_category_product')


@login_required
@permission_required(perm='Shop.add_subcategory')
def panel_add_subcategory_product(request):
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
    if not request.user.is_staff:
        return redirect('index')
    SubCategory.objects.using('shop').get(pk=pk).delete()
    return redirect('panel_add_subcategory_product')


@login_required
@permission_required(perm='Shop.add_product')
def panel_add_product(request):
    if not request.user.is_staff:
        return redirect('index')
    groups = Group.objects.using('shop').all()
    categories = Category.objects.using('shop').all()
    subcategories = SubCategory.objects.using('shop').all()
    if request.method == 'POST':
        title = request.POST.get('title')
        title_english = request.POST.get('title_english')
        group = request.POST.get('group')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        GCS = subcategories.using('shop').filter(category=category, group=group,
                                                 name=subcategory)  # G=group C=category S=subcategory
        print(GCS, group, category, subcategory, subcategories)
        if len(GCS) == 0:
            return redirect('panel_add_product')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')
        video = request.FILES.get('video')
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
        Product.objects.using('shop').create(description=description, name_product=title,
                                             name_product_english=title_english, group=GCS[0].group,
                                             group_id=GCS[0].group_id, category=GCS[0].category,
                                             category_id=GCS[0].category_id,
                                             sub_category=subcategory, sub_category_id=GCS[0].pk, color=color,
                                             size=size,
                                             image1=image1, image2=image2, image3=image3, image4=image4, video=video,
                                             attribute_title=input_title, attribute_value=input_value, price=price,
                                             discount_percent=float(percent), number=number, discount_period=to_day,
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
    if not request.user.is_staff:
        return redirect('index')
    if not request.user.is_authenticated or not request.user.is_staff or not request.user.is_active:
        return redirect('index')
    product = Product.objects.using('shop').get(pk=pk)
    groups = Group.objects.using('shop').all()
    categories = Category.objects.using('shop').all()
    subcategories = SubCategory.objects.using('shop').all()
    if request.method == 'POST':
        subcategories = SubCategory.objects.using('shop').all()
        title = request.POST.get('new_title')
        title_english = request.POST.get('new_title_english')
        group = request.POST.get('new_group')
        category = request.POST.get('new_category')
        subcategory = request.POST.get('new_subcategory')
        GCS = subcategories.filter(category=category, group=group, name=subcategory)  # G=group C=category S=subcategory
        if len(GCS) == 0:
            return redirect('panel_add_product')
        image1 = request.FILES.get('new_image1')
        image2 = request.FILES.get('new_image2')
        image3 = request.FILES.get('new_image3')
        image4 = request.FILES.get('new_image4')
        video = request.FILES.get('new_video')
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
        edit_product.discount_percent = float(percent)
        edit_product.name_product_english = title_english
        edit_product.name_product = title
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
    title_text = eval(product.title_text)
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
    if not request.user.is_staff:
        return redirect('index')
    products = Product.objects.using('shop').order_by('-date')
    context = {'products': products}
    return render(request, 'back/PanelShop/list_product.html', context=context)


@login_required
@permission_required(perm='Shop.delete_product')
def panel_delete_product(request, pk):
    if not request.user.is_staff:
        return redirect('index')
    product = Product.objects.using('shop').get(pk=pk)
    product.delete(using='shop')
    return redirect('panel_list_product')


@login_required
@permission_required(perm='Shop.change_subcategory')
def panel_edit_subcategory_product(request, pk):
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
        subcategory_edit.save(using='blog')
        return redirect('panel_add_subcategory_product')
