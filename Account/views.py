from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Permission, Group
from django.contrib import auth
from django.conf import settings
from django.core.signing import Signer
from django.core.cache import caches
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, permission_required
import random
from .forms import SigninForm, SignupForm
from .models import CustomUser


# Create your views here.
def signin(request):  # User login function
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
            else:
                messages.error(request, 'user not exist')
                return redirect('signin')
            # Encrypting the user's pk and transferring it to the site's cache
            data = Signer(key='drv%&8nl$#%v*)_1n*g+!0k4k3ru&nb!&pfm3-h3mb%@&=yvo&')
            caches['mycache'].set('my_site', data.sign_object(request.user.pk))
            if not user.is_active:  # Account activation notification
                messages.warning(request, 'Please activate your account')
            else:
                messages.success(request, 'success login')
            return redirect('profile_dashboard')
    form = SigninForm()
    return render(request, 'front/User/signin.html', {'form': form})


def verify_email(request):
    # Email verification function
    if request.method == 'POST':
        value2 = request.POST.get('value21') + request.POST.get('value22') + request.POST.get(
            'value23') + request.POST.get('value24') + request.POST.get(
            'value25')  # Creating the code entered by the user
        username = request.session['username']
        # Getting the verification code from the user model
        user = CustomUser.objects.get(username=username)
        value1 = user.verify_code
        if value2 == value1:  # Matching the verification code entered by the user and the existing code in the database
            user.is_active = True  # Convert inactive user to active user
            user.save()
            return redirect('signin')
        else:
            context = {'username': username}
            return render(request, "front/User/verify_email.html", context=context)
    return render(request, "front/User/verify_email.html")


def send_mail_custom(request, datas):
    # The function of sending an email containing a confirmation code
    x = ''.join((random.choice('0123456789') for i in range(5)))  # Creating a verification code
    request.session['username'] = datas['username']
    send_mail(subject='moji', message=f'hi moji {x}', from_email=settings.EMAIL_HOST_USER,
              recipient_list=[datas['email']])  # Send email
    return x


def signup(request):  # User registration function
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        datas = form.data
        if CustomUser.objects.filter(username=datas['username'], is_active=False).exists():
            # If there is a user with an inactive username and status, it will go to the email confirmation section
            code = send_mail_custom(request, datas)
            user = CustomUser.objects.get(username=datas['username'])
            user.verify_code = code
            user.save()
            context = {'username ': datas['username']}
            return render(request, 'front/User/verify_email.html', context=context)
        elif form.is_valid():
            if datas['password'] == datas['confirm_password']:  # Check if the entered passwords are the same
                code = send_mail_custom(request, datas)
                user = form.save()
                user.is_active = False  # Disable the created user
                user.verify_code = code  # Store the verification code in the user model
                user.save()
                context = {'username': datas['username']}
                return render(request, 'front/User/verify_email.html', context=context)
        else:
            redirect('signup')
    form = SignupForm()
    return render(request, "front/User/signup.html", {'form': form})


def signout(request):  # User exit function
    logout(request)
    messages.success(request, 'شما با موفقیت خارج شدید')
    caches['mycache'].clear()
    return redirect('index')


######################################## Panel #############################################
@login_required
@permission_required(perm='Account.view_CustomUser')
def panel_list_user(request):
    if not request.user.is_staff:
        return redirect('index')
    users = CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'back/PanelUser/user_list.html', context=context)


@login_required
@permission_required(perm='auth.view_permission')
def panel_permissions(request, pk):
    if not request.user.is_staff:
        return redirect('index')

    user = CustomUser.objects.get(pk=pk)
    groups = Group.objects.all()
    groups_user = Group.objects.filter(user=user)
    permissions = Permission.objects.all()
    permissions_user = Permission.objects.filter(user=user)
    context = {'permissions_user': permissions_user,
               'permissions': permissions, 'groups_user': groups_user,
               'groups': groups,
               'user': user}
    return render(request, 'back/PanelUser/permissions.html', context=context)


@login_required
@permission_required(perm='auth.view_group')
def panel_add_group_user(request):
    if not request.user.is_staff:
        return redirect('index')

    permissionss = Permission.objects.all()
    groups = Group.objects.all()
    if request.method == 'POST':
        name_group = request.POST.get('name_group')
        perms = request.POST.getlist('perms')
        perms_obj = Permission.objects.filter(pk__in=perms)
        new_group = Group(name=name_group)
        new_group.save()
        new_group.permissions.add(*perms_obj)
        new_group.save()
        return redirect('panel_add_group_user')
    context = {'permissions': permissionss, 'groups': groups}
    return render(request, 'back/PanelUser/panel_add_group_user.html', context=context)


@login_required
@permission_required(perm='auth.delete_group')
def panel_delete_group_user(request, pk):
    if not request.user.is_staff:
        return redirect('index')
    Group.objects.get(pk=pk).delete()
    return redirect('panel_add_group_user')


@login_required
@permission_required(perm='auth.add_permission')
def panel_user_access(request, pk):
    if not request.user.is_staff:
        return redirect('index')
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=pk)
        staff = request.POST.get('staff')
        super_user = request.POST.get('super_user')
        active = request.POST.get('active')
        if staff == 'on':
            user.is_staff = True
        else:
            user.is_staff = False
        if super_user == 'on':
            user.is_superuser = True
        else:
            user.is_superuser = False
        if active == 'on':
            user.is_active = True
        else:
            user.is_active = False
        perms = request.POST.getlist('perms')
        groups = request.POST.getlist('groups')
        groups_list = Group.objects.filter(pk__in=groups)
        perm_list = Permission.objects.filter(pk__in=perms)
        user.user_permissions.clear()
        user.groups.clear()
        user.user_permissions.add(*perm_list)
        user.groups.add(*groups_list)
        user.save()
        return redirect('panel_permissions', pk=pk)


@login_required
@permission_required(perm='auth.view_group')
def panel_details_group(request, pk=None):
    if not request.user.is_staff:
        return redirect('index')

    group = Group.objects.get(pk=pk)
    perms_grope = group.permissions.all()
    permissions = Permission.objects.all()
    if request.method == 'POST':
        title = request.POST.get('name_title')
        new_perms = request.POST.getlist('new_perms')
        group.permissions.clear()
        group.name = title
        group.permissions.add(*new_perms)
        group.save()
        return redirect('panel_details_group', pk=pk)

    return render(request, 'back/PanelUser/details_group.html',
                  {'group': group, 'permissions': permissions, 'perms_grope': perms_grope})


@login_required
@permission_required(perm='auth.delete_user')
def panel_delete_user(request, pk):
    if not request.user.is_staff:
        return redirect('index')
    CustomUser.objects.get(pk=pk).delete()
    return redirect('panel_list_user')
