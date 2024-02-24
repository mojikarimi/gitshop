from __future__ import unicode_literals
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from Account.models import CustomUser
from Main.models import Visit, ChatNew, Slider, Gif, Trend
from Main.models import MainModel, Menu, CatFooter, SubCatFooter, Footer
from Profile.models import Tickets, AnswerTicket
from jdatetime import datetime, timedelta
from .models import ChatRoom
from ipware import get_client_ip
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from Shop.models import Product

from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.
def index(request):
    gif = Gif.objects.all().first()
    sliders = Slider.objects.all()
    best_sellers= Product.objects.order_by('sales_number')
    instant_sales= Product.objects.filter(instant_sale=True).order_by('instant_sale')
    instant_sales_reverse = Product.objects.filter(instant_sale=True).order_by('-instant_sale')
    our_suggestions=Product.objects.filter(our_suggestion=True)[:9]

    if Visit.objects.filter(x=str(datetime.now())[:10]):
        obj = Visit.objects.get(x=str(datetime.now())[:10])
        obj.y += 1
        obj.save()
    else:
        visit = Visit(x=str(datetime.now())[:10], y=1)
        visit.save()
    return render(request, "front/Main/index.html", {'gif': gif, 'sliders': sliders})


def new_chat(request):
    # This function creates a new chat, it creates a chat room and the first message

    if request.method == 'POST':
        message = request.POST.get('message')  # It gets the message
        room = ChatRoom.objects.filter(user=request.user, ip_client=get_client_ip(request)[0])
        # Among all the rooms, it takes the room that has the same IP and username user
        if len(room) == 0:  # We will check the number of members so that if there is no room, one will be created
            room = ChatRoom(user=request.user, ip_client=get_client_ip(request)[0])  # creat room
            room.save()
        else:
            room = room[0]  # get a room
        date_active = datetime.now() + timedelta(days=1)  # A date that can be displayed to anonymous users
        chatnew = ChatNew(room=room, text=message, type='client', date_active=date_active,
                          status='اعلام نشده')  # Creating a message model
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


########################################### panel ##########################################

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
    if request.method == 'POST':
        cat = CatFooter.objects.get(pk=pk)
        subcats = SubCatFooter.objects.filter(cat_id=pk)
        title = request.POST.get('title')
        cat.title = title
        cat.save()
        for i in subcats:
            i.cat = title
            i.save()
        return redirect('panel_add_cat_footer')

@login_required
@permission_required(perm='Main.delete_chatfooter')
def panel_delete_cat_footer(request, pk):
    cat = CatFooter.objects.get(pk=pk)
    subcats = SubCatFooter.objects.filter(cat_id=pk)
    subcats.delete()
    cat.delete()
    return redirect('panel_add_cat_footer')

@login_required
@permission_required(perm='Main.add_subchatfooter')
def panel_add_subcat_footer(request, pk):
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
    subcat = SubCatFooter.objects.get(pk=pk)
    subcat.delete()
    return redirect('panel_add_subcat_footer', pk=pk)

@login_required
@permission_required(perm='Main.change_subchatfooter')
def panel_edit_subcat_footer(request, pk):
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
    menu = Menu.objects.get(pk=pk)
    menu.delete()
    return redirect('panel_add_menu')

@login_required
@permission_required(perm='Main.add_menu')
def panel_sort_menu(request):
    if request.method == 'POST':
        menus = Menu.objects.all()
        sorts = request.POST.getlist('sort')
        for i, x in enumerate(sorts):
            menu = menus.get(pk=x)
            menu.number = i
            menu.save()
        return redirect('panel_add_menu')

@login_required
@permission_required(perm='Main.add_footer')
def panel_footer(request):
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
        if image1:
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
    main = MainModel.objects.all().first()
    if request.method == 'POST':
        icon = request.FILES.get('icon')
        logo = request.FILES.get('logo')
        title_website = request.POST.get('title_website')
        title_panel = request.POST.get('title_panel')
        if icon:
            main.icon = icon
            main.save()
        if logo:
            main.logo = logo
            main.save()
        main.title_website = title_website
        main.title_panel = title_panel
        return redirect('panel_main_model')
    return render(request, 'back/PanelMain/panel_main_model.html')

@login_required
@permission_required(perm='Main.add_tickets')
def panel_tickets_lists(request):
    tickets = Tickets.objects.using('profile').order_by('-date')
    context = {'tickets': tickets, 'closed': len(tickets.filter(status='بسته شده')),
               'invalid': len(tickets.filter(status='غیر قابل قبول')),
               'answered': len(tickets.filter(status='پاسخ داده شده')),
               'pending': len(tickets.filter(status='درحال بررسی')), }
    return render(request, "back/PanelMain/panel_tickets.html", context=context)

@login_required
@permission_required(perm='Main.add_answerticket')
def panel_answer_tickets(request, pk):
    ticket = Tickets.objects.using('profile').get(pk=pk)
    answers_tickets = AnswerTicket.objects.using('profile').order_by('-date').filter(ticket=ticket)
    context = {'ticket': ticket, 'answers_tickets': answers_tickets, }
    if request.method == 'POST':
        type_user = request.POST.get('type_user')
        text = request.POST.get('text')
        answerticket = AnswerTicket(ticket=ticket, type_user=type_user, text=text, user_id=request.user.pk,
                                    user=request.user.username)
        answerticket.save(using='profile')
        ticket.date_update = datetime.now()
        ticket.status = 'پاسخ داده شده'
        ticket.save(using='profile')
        return redirect('panel_tickets_lists')
    return render(request, "back/PanelMain/panel_answer_tickets.html", context=context)

@login_required
@permission_required(perm='Main.view_tickets')
def panel_change_status_ticket(request, pk):
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
    if request.method == 'POST':
        main_gif = Gif.objects.all().first()
        gif = request.FILES.get('gif')
        link = request.POST.get('link')
        if gif:
            main_gif.gif = gif
        main_gif.link = link
        main_gif.save()
        return redirect('panel_gif')
    main_gif = Gif.objects.all().first()
    return render(request, 'back/PanelMain/panel_gif.html', {'main_gif': main_gif})

@login_required
@permission_required(perm='Main.add_slider')
def panel_add_slider(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        image = request.FILES.get('image')
        try:
            fs = FileSystemStorage(location=f'{settings.MEDIA_ROOT}/Main/slider/')
            filename = fs.save(image.name, image)
            if str(image.content_type).startswith('image'):
                if image.size <= 5242880:
                    image = filename
                    image_url = f'{settings.MEDIA_URL}' + 'Main/slider/' + image
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
    slider = Slider.objects.get(pk=pk)
    if request.method == 'POST':
        link = request.POST.get('link')
        try:
            image = request.FILES.get('image')
            fs = FileSystemStorage(location=f'{settings.MEDIA_ROOT}/Main/slider/')
            filename = fs.save(image.name, image)
            if str(image.content_type).startswith('image'):
                if image.size <= 5242880:
                    image = filename
                    image_url = f'{settings.MEDIA_URL}' + 'Main/slider/' + image
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
            slider.link = link
            slider.save()
            messages.success(request, 'Changes applied successfully')
            return redirect('panel_add_slider')
    return render(request, 'back/PanelMain/panel_edit_slider.html', {'slider': slider})

@login_required
@permission_required(perm='Main.delete_slider')
def panel_delete_slider(request, pk):
    slider = Slider.objects.get(pk=pk)
    slider.delete()
    return redirect('panel_add_slider')

@login_required
@permission_required(perm='Main.add_trend')
def panel_trend(request):
    trend = Trend.objects.all().first()
    if request.method == 'POST':
        status = request.POST.get('status')
        link = request.POST.get('link')
        if status == 'on':
            status = 1
        else:
            status = 0
        try:
            image = request.FILES.get('image')
            fs = FileSystemStorage(location=f'{settings.MEDIA_ROOT}/Main/trend/')
            filename = fs.save(image.name, image)
            if str(image.content_type).startswith('image'):
                if image.size <= 5242880:
                    image = filename
                    image_url = f'{settings.MEDIA_URL}' + 'Main/trend/' + image
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
            trend.link = link
            trend.status = status
            trend.save()
            messages.success(request, 'Changes applied successfully')
            return redirect('panel_trend')
    return render(request, 'back/PanelMain/panel_trend.html', {'trend': trend})
