from Main.models import MainModel, Menu, ChatNew, ChatRoom, Footer, CatFooter, SubCatFooter, Trend
from ipware import get_client_ip


def context_processor(request):
    main = MainModel.objects.all().first()
    menus = Menu.objects.order_by('number')
    footer = Footer.objects.all().first()
    trend = Trend.objects.all().first()
    catfooters = CatFooter.objects.all()
    subcatfooters = SubCatFooter.objects.all()
    return {'main': main, 'menus': menus, 'footer': footer, 'trend': trend, 'catfooters': catfooters,
             'subcatfooters': subcatfooters}


def context_processor_chat(request):
    # To display messages in all sections of the site
    chatroom = ChatRoom.objects.filter(user=request.user, ip_client=get_client_ip(request)[0])
    if len(chatroom) > 0:
        chats = ChatNew.objects.filter(room=chatroom[0])
        if str(request.user) == 'AnonymousUser':
            # Delete messages from anonymous users after a day
            for i in chats:
                if i.date >= i.date_active:
                    i.delete()
    else:
        chats = None
    return {'chats': chats}
