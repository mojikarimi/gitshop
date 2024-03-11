from Main.models import MainModel, Menu, ChatNew, ChatRoom, Footer, CatFooter, SubCatFooter, Trend,Symbol,Social_Networks
from Shop.models import Cart, ProductCart, Product, Group, Category, SubCategory
from ipware import get_client_ip


def context_processor(request):
    main = MainModel.objects.all().first()
    menus = Menu.objects.order_by('number')
    footer = Footer.objects.all().first()
    trend = Trend.objects.all().first()
    catfooters = CatFooter.objects.all()
    subcatfooters = SubCatFooter.objects.all()
    symbols = Symbol.objects.all()
    social_networks = Social_Networks.objects.all()
    groups = Group.objects.using('shop').all()
    categories = Category.objects.using('shop').all()
    subcategories = SubCategory.objects.using('shop').all()
    context = {'main': main, 'menus': menus, 'footer': footer, 'trend': trend, 'catfooters': catfooters,
               'subcatfooters': subcatfooters,'symbols':symbols ,'social_networks':social_networks,'groups': groups, 'categories': categories,
               'subcategories': subcategories}
    try:
        context_processor_carts = Cart.objects.using('shop').filter(user_id=request.user.pk, status=False).first()
        product_carts = ProductCart.objects.using('shop').filter(cart_id=context_processor_carts.pk)
        products = Product.objects.using('shop').filter(pk__in=product_carts.values('product_id'))
        context['context_processor_carts'] = context_processor_carts
        context['product_carts'] = product_carts
        context['products'] = products
    except:
        pass
    return context


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
