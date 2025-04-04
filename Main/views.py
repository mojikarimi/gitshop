from __future__ import unicode_literals
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from Account.models import CustomUser
from Main.models import Visit, ChatNew, Slider, Gif, Trend, EmailShare, Symbol, Social_Networks
from Main.models import MainModel, Menu, CatFooter, SubCatFooter, Footer
from Profile.models import Tickets, AnswerTicket
from jdatetime import datetime, timedelta
from .models import ChatRoom, FAQCategory
from ipware import get_client_ip
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from Shop.models import Product, Question

from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
def faq(request):
    # see category FAQ
    faq_categories = FAQCategory.objects.all()
    faqs = Question.objects.filter(faq=True, status=True).order_by('sort')
    context = {'faq_categories': faq_categories, 'faqs': faqs}
    return render(request, 'front/Main/faq.html', context=context)


def faq_details(request, category):
    # see details Category
    faq_details_category = Question.objects.filter(category=category)
    faqs = Question.objects.filter(faq=True, status=True).order_by('sort')
    category = FAQCategory.objects.get(name=category)
    context = {'faq_details_category': faq_details_category, 'faqs': faqs, 'category': category}
    return render(request, 'front/Main/faq_details.html', context=context)


def index(request):
    # for index page
    gif = Gif.objects.all().first()
    sliders = Slider.objects.all()
    instant_sales = Product.objects.using('shop').filter(instant_sale=True).order_by('instant_sale')[:5]
    best_sellers = Product.objects.using('shop').order_by('sales_number')
    best_sellers_reverse = Product.objects.using('shop').order_by('-sales_number')
    our_suggestions = Product.objects.filter(our_suggestion=True)[:9]

    if Visit.objects.filter(x=str(datetime.now())[:10]):
        obj = Visit.objects.get(x=str(datetime.now())[:10])
        obj.y += 1
        obj.save()
    else:
        visit = Visit(x=str(datetime.now())[:10], y=1)
        visit.save()
    return render(request, "front/Main/index.html",
                  {'gif': gif, 'sliders': sliders, 'instant_sales': instant_sales, 'best_sellers': best_sellers,
                   'best_sellers_reverse': best_sellers_reverse, 'our_suggestions': our_suggestions})


def new_chat(request):
    # This function creates a new chat, it creates a chat room and the first message

    if request.method == 'POST':
        message = request.POST.get('message')  # It gets the message
        room = ChatRoom.objects.filter(user=request.user, ip_client=get_client_ip(request)[0])
        # Among all the rooms, it takes the room that has the same IP and username user
        if len(room) == 0:  # We will check the number of members so that if there is no room, one will be created
            room = ChatRoom(user=request.user, ip_client=get_client_ip(request)[0], status='اعلام نشده')  # creat room
            room.save()
        else:
            room = room[0]  # get a room

        date_active = datetime.now() + timedelta(days=1)  # A date that can be displayed to anonymous users
        chatnew = ChatNew(room=room, text=message, type='client', date_active=date_active)  # Creating a message model
        chatnew.save()
        message = ChatNew.objects.filter(pk=chatnew.pk)
        message = serializers.serialize('json', message)  # Convert message models to json file
        return JsonResponse({'message': message})


def update_chat(request):
    # This function checks for new messages
    if request.method == 'POST':
        chatroom = ChatRoom.objects.filter(ip_client=get_client_ip(request)[0],
                                           user=request.user).first()  # get a room with pk
        messages = ChatNew.objects.filter(room=chatroom, status=False, type='admin')  # Get messages
        for i in messages:
            i.status = True
            # Changes the status of messages to read
            i.save()
        if chatroom:
            admin = chatroom.admin  # We take the name of the admin
            status = chatroom.status  # We take the state of the room
            messages = serializers.serialize('json', messages)  # Convert message models to json file
            return JsonResponse({'messages': messages, 'admin': admin, 'status': status})
        return JsonResponse({})


def email_shair(request):
    # To save the emails that the user enters
    if request.method == 'POST':
        email = request.POST.get('email')
        EmailShare.objects.create(email=email)
        return redirect(request.META['HTTP_REFERER'])


########################################### panel ##########################################
@login_required
@permission_required(perm='Main.add_FAQCategory')
def panel_add_faq_category(request):
    # for add group product
    if not request.user.is_staff:
        return redirect('index')
    faq_categories = FAQCategory.objects.all()
    if request.method == 'POST':
        faq_category = request.POST.get('faq_category')
        if len(faq_categories.filter(
                name=faq_category)) >= 1:  # Calculation of the number of categories with this title
            # messages.error(request, 'There is a category with this title')
            return redirect('panel_add_faq_category')

        image = request.FILES.get('image')
        if image:
            if str(image.content_type).startswith('image'):
                if image.size <= 5242880:  # The size of the photo must be less than 5 MB
                    FAQCategory.objects.create(image=image, name=faq_category)
                    messages.success(request, 'Successfully added')
                    return redirect('panel_add_faq_category')
                else:
                    messages.error(request, 'More volume than the permissible limit')
                    return redirect('panel_add_faq_category')
            else:
                messages.error(request, 'The photo format is incorrect')
                return redirect('panel_add_faq_category')
        else:
            messages.error(request, 'The photo is not available')
            return redirect('panel_add_faq_category')

    context = {'faq_categories': faq_categories}
    return render(request, 'back/PanelMain/add_faq_category.html', context=context)


@login_required
@permission_required(perm='Shop.change_group')
def panel_edit_faq_category(request, pk):
    # for edit group product
    if not request.user.is_staff:
        return redirect('index')

    if request.method == 'POST':
        faq_category_new = request.POST.get('faq_category_new')
        if len(FAQCategory.objects.filter(~Q(pk=pk),
                                          name=faq_category_new)) >= 1:  # Calculation of the number of categories with this title
            # messages.error(request, 'There is a category with this title')
            return redirect('panel_add_faq_category')
        faq_category_edit = FAQCategory.objects.get(pk=pk)
        # edit image category
        image = request.FILES.get('new_image')
        if image:  # update image
            if str(image.content_type).startswith('image'):
                if image.size <= 5242880:
                    faq_category_edit.image = image
                else:
                    messages.warning(request, 'More volume than the permissible limit')
                    return redirect('panel_add_faq_category')
            else:
                messages.warning(request, 'The photo format is incorrect')
                return redirect('panel_add_faq_category')
        faq_category_edit.name = faq_category_new
        faq_category_edit.save()
        messages.success(request, 'Successfully edited')
        return redirect('panel_add_faq_category')


@login_required
@permission_required(perm='Shop.delete_group')
def panel_delete_faq_category(request, pk):
    # for delete group product
    if not request.user.is_staff:
        return redirect('index')
    FAQCategory.objects.get(pk=pk).delete()
    return redirect('panel_add_faq_category')


def panel_change_status(request):
    # Function to change the status of the room from the admin side
    if request.method == 'POST':
        chatroom_pk = request.POST.get('chatroom_pk')
        chatroom = ChatRoom.objects.get(pk=chatroom_pk)
        chatroom.status = request.POST.get('status')  # Getting status from template side
        chatroom.save()
        return JsonResponse({'chatroom_pk': chatroom_pk})


def panel_new_chat(request):
    # Creating a message that the admin sends
    if request.method == 'POST':
        message = request.POST.get('message')
        chatroom_pk = request.POST.get('chatroom_pk')
        room = ChatRoom.objects.get(pk=chatroom_pk)
        room.admin = f'{request.user.first_name} {request.user.last_name}'  # Setting admin name and surname
        room.save()
        date_active = datetime.now() + timedelta(days=1)  # A date that can be displayed to anonymous users
        chatnew = ChatNew(room=room, text=message, type='admin', date_active=date_active)  # Create a chat
        chatnew.save()
        message = ChatNew.objects.filter(pk=chatnew.pk)
        message = serializers.serialize('json', message)  # Convert message models to json file
        return JsonResponse({'message': message, 'chatroom_pk': chatroom_pk})


def panel_update_chat(request):
    # Update panel messages
    if request.method == 'POST':
        chatroom_pk = request.POST.get('chatroom_pk')
        chatroom = ChatRoom.objects.get(pk=chatroom_pk)
        messages = ChatNew.objects.filter(room=chatroom, status=False, type='client')
        for i in messages:
            i.status = True  # Change status to read
            i.save()
        messages = serializers.serialize('json', messages)  # Convert message models to json file
        status = chatroom.status
        return JsonResponse({'chatroom_pk': chatroom_pk, 'messages': messages, 'status': status})


@login_required
@permission_required(perm='Main.view_chatroom')
def panel_chat(request):
    # Function to display chat rooms to the admin in the panel
    chatrooms = ChatRoom.objects.all()
    users = CustomUser.objects.filter(username__in=chatrooms.values('user'))  # In order to recognize anonymous users
    return render(request, 'back/PanelMain/panel_new_chat.html', context={'chatrooms': chatrooms, 'users': users})


@login_required
@permission_required(perm='Main.add_chatnew')
def panel_massages(request, pk):
    # To display the messages section in AppChat
    chatrooms = ChatRoom.objects.all()
    users = CustomUser.objects.filter(username__in=chatrooms.values('user'))
    chatroom = chatrooms.get(pk=pk)
    chats = ChatNew.objects.filter(room=chatroom).order_by('date')
    status = chatroom.status
    return render(request, 'back/PanelMain/panel_new_message.html',
                  context={'chatroom': chatroom, 'chats': chats, 'status': status, 'chatrooms': chatrooms,
                           'users': users})


@login_required
@permission_required(perm='Main.add_catfooter')
def panel_add_cat_footer(request):
    # for add category footer
    cats = CatFooter.objects.all()
    context = {'cats': cats}
    if request.method == 'POST':
        title = request.POST.get('title')
        cat = CatFooter(title=title)
        cat.save()
        return redirect('panel_add_cat_footer')
    return render(request, 'back/PanelMain/panel_add_cat_footer.html', context=context)


@login_required
@permission_required(perm='Main.change_chatfooter')
def panel_edit_cat_footer(request, pk):
    # for edit category footer
    if request.method == 'POST':
        cat = CatFooter.objects.get(pk=pk)
        subcats = SubCatFooter.objects.filter(cat_id=pk)
        title = request.POST.get('title')
        cat.title = title
        cat.save()
        for i in subcats:
            # for update sub category
            i.cat = title
            i.save()
        return redirect('panel_add_cat_footer')


@login_required
@permission_required(perm='Main.delete_chatfooter')
def panel_delete_cat_footer(request, pk):
    # for delete category footer
    cat = CatFooter.objects.get(pk=pk)
    subcats = SubCatFooter.objects.filter(cat_id=pk)
    subcats.delete()
    cat.delete()
    return redirect('panel_add_cat_footer')


@login_required
@permission_required(perm='Main.add_subchatfooter')
def panel_add_subcat_footer(request, pk):
    # for add new sub category footer and show list sub category footer
    subcats = SubCatFooter.objects.filter(cat_id=pk)
    cat = CatFooter.objects.get(pk=pk)
    context = {'subcats': subcats, 'cat': cat}
    if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('link')
        subcat = SubCatFooter(cat=cat.title, cat_id=cat.pk, title=title, link=link)
        subcat.save()
        return redirect('panel_add_subcat_footer', pk=pk)
    return render(request, 'back/PanelMain/panel_add_subcat_footer.html', context=context)


@login_required
@permission_required(perm='Main.delete_subchatfooter')
def panel_delete_subcat_footer(request, pk):
    # for delete sub category footer
    subcat = SubCatFooter.objects.get(pk=pk)
    subcat.delete()
    return redirect('panel_add_subcat_footer', pk=pk)


@login_required
@permission_required(perm='Main.change_subchatfooter')
def panel_edit_subcat_footer(request, pk):
    # for edit sub category footer
    if request.method == 'POST':
        subcat = SubCatFooter.objects.get(pk=pk)
        title = request.POST.get('title')
        link = request.POST.get('link')
        subcat.title = title
        subcat.link = link
        subcat.save()
        return redirect('panel_add_subcat_footer', pk=pk)


@login_required
@permission_required(perm='Main.add_menu')
def panel_add_menu(request):
    # for add new menu and show list menu
    menus = Menu.objects.order_by('number')
    context = {'menus': menus}
    if request.method == 'POST':
        menu_name = request.POST.get('menu_name')
        menu_link = request.POST.get('menu_link')
        menu = Menu(menu_name=menu_name, menu_link=menu_link)
        menu.save()
        return redirect('panel_add_menu')
    return render(request, 'back/PanelMain/panel_add_menu.html', context=context)


@login_required
@permission_required(perm='Main.change_menu')
def panel_edit_menu(request, pk):
    # for edit menu
    if request.method == 'POST':
        menu = Menu.objects.get(pk=pk)
        menu_name = request.POST.get('menu_name')
        menu_link = request.POST.get('menu_link')
        menu.menu_name = menu_name
        menu.menu_link = menu_link
        menu.save()
        return redirect('panel_add_menu')


@login_required
@permission_required(perm='Main.delete_menu')
def panel_delete_menu(request, pk):
    # for delete menu
    menu = Menu.objects.get(pk=pk)
    menu.delete()
    return redirect('panel_add_menu')


@login_required
@permission_required(perm='Main.add_menu')
def panel_sort_menu(request):
    # for sort menu
    if request.method == 'POST':
        menus = Menu.objects.all()
        sorts = request.POST.getlist('sort')
        for i, x in enumerate(sorts):  # sorts=[2,3,5] => 0->2 , 1->3 , 2->5
            menu = menus.get(pk=x)
            menu.number = i
            menu.save()
        return redirect('panel_add_menu')


@login_required
@permission_required(perm='Main.add_footer')
def panel_footer(request):
    # for footer main details(image,text,copy_right)
    footer_view = Footer.objects.all().first()
    if request.method == 'POST':
        footer = Footer.objects.all().first()
        copy_right = request.POST.get('copy_right')
        text = request.POST.get('text')
        image1_text = request.POST.get('image1_text')
        image1 = request.FILES.get('image1')
        image2_text = request.POST.get('image2_text')
        image2 = request.FILES.get('image2')
        image3_text = request.POST.get('image3_text')
        image3 = request.FILES.get('image3')
        image4_text = request.POST.get('image4_text')
        image4 = request.FILES.get('image4')
        image5_text = request.POST.get('image5_text')
        image5 = request.FILES.get('image5')
        link1 = request.POST.get('link1')
        link2 = request.POST.get('link2')
        link3 = request.POST.get('link3')
        link4 = request.POST.get('link4')
        link5 = request.POST.get('link5')
        if not footer:
            # To run the code the first time
            footer = Footer.objects.create()
        if image1:  # If the photo is sent or not, change it
            footer.image1 = image1
        if image2:
            footer.image2 = image2
        if image3:
            footer.image3 = image3
        if image4:
            footer.image4 = image4
        if image5:
            footer.image5 = image5
        footer.copy_right = copy_right
        footer.image1_text = image1_text
        footer.image2_text = image2_text
        footer.image3_text = image3_text
        footer.image4_text = image4_text
        footer.image5_text = image5_text
        footer.link1 = link1
        footer.link2 = link2
        footer.link3 = link3
        footer.link4 = link4
        footer.link5 = link5
        footer.text = text
        footer.save()
        return redirect('panel_footer')
    return render(request, 'back/PanelMain/panel_footer.html', {'footer_view': footer_view})


@login_required
@permission_required(perm='Main.add_mainmodel')
def panel_main_model(request):
    # for logo, icon, title panel and title panel
    main = MainModel.objects.all().first()
    if request.method == 'POST':
        icon = request.FILES.get('icon')
        logo = request.FILES.get('logo')
        title_website = request.POST.get('title_website')
        title_panel = request.POST.get('title_panel')
        if icon:
            main.icon = icon
        if logo:
            main.logo = logo
        main.title_website = title_website
        main.title_panel = title_panel
        main.save()

        return redirect('panel_main_model')
    return render(request, 'back/PanelMain/panel_main_model.html')


@login_required
@permission_required(perm='Main.add_tickets')
def panel_tickets_lists(request):
    # show tickets user
    tickets = Tickets.objects.using('profile').order_by('-date')
    context = {'tickets': tickets, 'closed': len(tickets.filter(status='بسته شده')),
               'invalid': len(tickets.filter(status='غیر قابل قبول')),  # Impossible number
               'answered': len(tickets.filter(status='پاسخ داده شده')),  # Number not answered
               'pending': len(tickets.filter(status='درحال بررسی')), }  # Number under review
    return render(request, "back/PanelMain/panel_tickets.html", context=context)


@login_required
@permission_required(perm='Main.add_answerticket')
def panel_answer_tickets(request, pk):
    # To respond to tickets
    ticket = Tickets.objects.using('profile').get(pk=pk)  # get ticket
    answers_tickets = AnswerTicket.objects.using('profile').order_by('-date').filter(
        ticket=ticket)  # get answers tocket
    context = {'ticket': ticket, 'answers_tickets': answers_tickets, }
    if request.method == 'POST':
        # for send answer ticket
        type_user = request.POST.get('type_user')
        text = request.POST.get('text')
        answerticket = AnswerTicket(ticket=ticket, type_user=type_user, text=text, user_id=request.user.pk,
                                    user=request.user.username)
        answerticket.save(using='profile')
        ticket.date_update = datetime.now()
        ticket.status = 'پاسخ داده شده'  # change status into answered
        ticket.save(using='profile')
        return redirect('panel_tickets_lists')
    return render(request, "back/PanelMain/panel_answer_tickets.html", context=context)


@login_required
@permission_required(perm='Main.view_tickets')
def panel_change_status_ticket(request, pk):
    # for change status tickets
    if request.method == 'POST':
        status = request.POST.get('status')
        ticket = Tickets.objects.get(pk=pk)
        ticket.status = status
        ticket.date_update = datetime.now()
        ticket.save(using='profile')
        return redirect('panel_tickets_lists')


@login_required
@permission_required(perm='Main.add_gif')
def panel_gif(request):
    # for add and edit gif in index page
    if request.method == 'POST':
        main_gif = Gif.objects.all()
        gif = request.FILES.get('gif')
        link = request.POST.get('link')
        if main_gif:
            if gif:
                main_gif[0].gif = gif
            main_gif[0].link = link
            main_gif[0].save()
        else:
            main_gif.create(gif=gif, link=link)
        return redirect('panel_gif')
    main_gif = Gif.objects.all().first()
    return render(request, 'back/PanelMain/panel_gif.html', {'main_gif': main_gif})


@login_required
@permission_required(perm='Main.add_slider')
def panel_add_slider(request):
    # for add new slider to index page
    if request.method == 'POST':
        link = request.POST.get('link')
        image = request.FILES.get('image')
        try:  # use FileSystemStorage for upload image
            fs = FileSystemStorage(location=f'{settings.MEDIA_ROOT}/Main/slider/')  # Give the path to save the photo
            filename = fs.save(image.name, image)
            if str(image.content_type).startswith('image'):
                if image.size <= 5242880:
                    image = filename
                    image_url = f'{settings.MEDIA_URL}' + 'Main/slider/' + image  # Give the path to save the photo
                    slider = Slider(image=image, image_url=image_url, link=link)
                    slider.save()
                    messages.success(request, 'Added successfully')
                else:
                    fs.delete(filename)
                    messages.error(request, 'The size of the photo is large')
            else:
                fs.delete(filename)
                messages.error(request, 'The file format is not correct')
        finally:
            return redirect('panel_add_slider')
    sliders = Slider.objects.all()
    return render(request, 'back/PanelMain/panel_add_slider.html', {'sliders': sliders})


@login_required
@permission_required(perm='Main.change_slider')
def panel_edit_slider(request, pk):
    # for edit slider in index page
    slider = Slider.objects.get(pk=pk)
    if request.method == 'POST':
        link = request.POST.get('link')
        try:  # use FileSystemStorage for upload image
            image = request.FILES.get('image')
            fs = FileSystemStorage(location=f'{settings.MEDIA_ROOT}/Main/slider/')  # Give the path to save the photo
            filename = fs.save(image.name, image)
            if str(image.content_type).startswith('image'):
                if image.size <= 5242880:
                    image = filename
                    image_url = f'{settings.MEDIA_URL}' + 'Main/slider/' + image  # Give the path to save the photo
                    slider.image = image
                    slider.image_url = image_url
                else:
                    fs.delete(filename)
                    messages.error(request, 'The size of the photo is large')
                    return redirect('panel_edit_slider', pk=pk)
            else:
                fs.delete(filename)
                messages.error(request, 'The file format is not correct')
                return redirect('panel_edit_slider', pk=pk)
        finally:
            # set link for slider
            slider.link = link
            slider.save()
            messages.success(request, 'Changes applied successfully')
            return redirect('panel_add_slider')
    return render(request, 'back/PanelMain/panel_edit_slider.html', {'slider': slider})


@login_required
@permission_required(perm='Main.delete_slider')
def panel_delete_slider(request, pk):
    # for delete slider
    slider = Slider.objects.get(pk=pk)
    slider.delete()
    return redirect('panel_add_slider')


@login_required
@permission_required(perm='Main.add_trend')
def panel_trend(request):
    # for add trend and edit its
    trend = Trend.objects.all().first()
    if request.method == 'POST':
        status = request.POST.get('status')
        link = request.POST.get('link')
        if not trend:
            # To run the code the first time
            trend = Trend.objects.create()
        # To be displayed or not
        if status == 'on':
            status = 1
        else:
            status = 0
        try:  # use FileSystemStorage for upload image
            image = request.FILES.get('image')
            fs = FileSystemStorage(location=f'{settings.MEDIA_ROOT}/Main/trend/')  # Give the path to save the photo
            filename = fs.save(image.name, image)
            if str(image.content_type).startswith('image'):
                if image.size <= 5242880:
                    image = filename
                    image_url = f'{settings.MEDIA_URL}' + 'Main/trend/' + image  # Give the path to save the photo
                    trend.image = image
                    trend.image_url = image_url
                else:
                    fs.delete(filename)
                    messages.error(request, 'The size of the photo is large')
                    return redirect('panel_trend')
            else:
                fs.delete(filename)
                messages.error(request, 'The file format is not correct')
                return redirect('panel_trend')
        finally:
            # set link and status to trend
            trend.link = link
            trend.status = status
            trend.save()
            messages.success(request, 'Changes applied successfully')
            return redirect('panel_trend')
    return render(request, 'back/PanelMain/panel_trend.html', {'trend': trend})


@login_required
@permission_required(perm='Main.add_symbol')
def panel_add_symbol(request):
    # for add A symbol
    symbols = Symbol.objects.all()
    if request.method == 'POST':
        image = request.FILES.get('image')  # symbol
        link = request.POST.get('link')  # symbol link
        Symbol.objects.create(image=image, link=link)
        return redirect('panel_add_symbol')
    return render(request, 'back/PanelMain/panel_add_symbol.html', {'symbols': symbols})


@login_required
@permission_required(perm='Main.change_symbol')
def panel_edit_symbol(request, pk):
    # for edit symbol with pk
    if request.method == 'POST':
        image_new = request.FILES.get('image_new')  # new image  for symbol
        link_new = request.POST.get('link_new')  # new link  for symbol
        symbol = Symbol.objects.get(pk=pk)
        if image_new:
            symbol.image = image_new
        symbol.link = link_new
        symbol.save()
        return redirect('panel_add_symbol')


@login_required
@permission_required(perm='Main.delete_symbol')
def panel_delete_symbol(request, pk):
    # for delete a symbol with pk
    symbol = Symbol.objects.get(pk=pk)
    symbol.delete()
    return redirect('panel_add_symbol')


@login_required
@permission_required(perm='Main.add_social_networks')
def panel_add_social_networks(request):
    # for add a social network
    social_networks = Social_Networks.objects.all() # getting all social networks
    if request.method == 'POST':
        icon = request.POST.get('icon')
        link = request.POST.get('link')
        Social_Networks.objects.create(icon=icon, link=link)
        return redirect('panel_add_social_networks')
    return render(request, 'back/PanelMain/panel_add_social_networks.html', {'social_networks': social_networks})

@login_required
@permission_required(perm='Main.change_social_networks')
def panel_edit_social_networks(request, pk):
    # for edit social network with pk
    if request.method == 'POST':
        icon_new = request.POST.get('icon_new')
        link_new = request.POST.get('link_new')
        social_network = Social_Networks.objects.get(pk=pk)
        social_network.link = link_new
        social_network.icon = icon_new
        social_network.save()
        return redirect('panel_add_social_networks')

@login_required
@permission_required(perm='Main.delete_social_networks')
def panel_delete_social_networks(request, pk):
    # for delete social_networks with pk
    social_network = Social_Networks.objects.get(pk=pk)
    social_network.delete()
    return redirect('panel_add_social_networks')
