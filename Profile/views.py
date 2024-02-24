from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
import random
from django.core.mail import send_mail
# Create your views here.
from jdatetime import datetime
from django.conf import settings
from Profile.models import Tickets, AnswerTicket
from Account.models import CustomUser
from django.contrib.auth.decorators import login_required


@login_required
def profile_dashboard(request):
    if request.method == 'POST':
        x = ''.join((random.choice('0123456789') for _ in range(5)))  # Creating a verification code
        request.session['username'] = request.user.username
        user = CustomUser.objects.get(pk=request.user.pk)
        user.verify_code = x
        user.save()
        send_mail(subject='moji', message='hi moji ' + x, from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[request.user.email])  # Send email
        return redirect('verify_email')
    myuser = CustomUser.objects.get(pk=request.user.pk)
    return render(request, 'front/Profile/profile_dashboard.html', {'myuser': myuser, })


@login_required
def profile_personal_info(request):
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
        if email != myuser.email:
            x = ''.join((random.choice('0123456789') for _ in range(5)))
            # Creating a verification code
            request.session['username'] = request.user.username
            myuser.verify_code = x
            myuser.is_active = False
            myuser.email = email
            myuser.save()
            send_mail(subject='moji', message='hi moji ' + x, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[request.user.email])  # Send email
            return redirect('verify_email')
        else:
            myuser.save()
            return redirect('profile_personal_info')

    return render(request, 'front/Profile/profile_personal_info.html', {'myuser': myuser, })


@login_required
def profile_tickets(request):
    if not request.user.is_active:  # Account activation notification
        messages.warning(request, 'Please activate your account')
        return redirect('profile_dashboard')
    myuser = CustomUser.objects.get(pk=request.user.pk)
    parts = Group.objects.using('profile').all()
    tickets = Tickets.objects.using('profile').order_by('-date').filter(user_id=request.user.pk)
    for i in tickets.filter(status='درحال بررسی'):

        if ((int(datetime.now().year) * 365) + (int(datetime.now().month) * 30) + (int(datetime.now().day))) - (
                (int(i.date[:4]) * 365) + (int(i.date[5:7]) * 30) + (int(i.date[8:10]))) >= 10:
            i.status = 'بسته شده'
            i.save(using='profile')
    context = {'parts': parts, 'tickets': tickets, 'myuser': myuser}
    if request.method == 'POST':
        subject = request.POST.get('subject')
        part = request.POST.get('part')
        text = request.POST.get('text')
        part_name = Group.objects.get(pk=part)
        ticket = Tickets(subject=subject, text=text, manager=part_name.name, manager_id=part,
                         user=request.user.username, user_id=request.user.pk, status='درحال بررسی')
        ticket.save(using='profile')
        ticket.ticket_id = ticket.pk + 100000
        ticket.save(using='profile')
        return redirect('profile_tickets')
    return render(request, 'front/Profile/profile_tickets.html', context=context)


@login_required
def profile_detail_tickets(request, pk):
    if not request.user.is_active:  # Account activation notification
        messages.warning(request, 'Please activate your account')
        return redirect('profile_dashboard')
    myuser = CustomUser.objects.get(pk=request.user.pk)
    ticket = Tickets.objects.using('profile').get(pk=pk, user_id=request.user.pk)
    answertickets = AnswerTicket.objects.using('profile').order_by('-date').filter(ticket=ticket)
    context = {'ticket': ticket, 'answertickets': answertickets, 'number': len(answertickets), 'myuser': myuser}
    if request.method == 'POST':
        text = request.POST.get('text')
        type_user = request.POST.get('type_user')
        answerticket = AnswerTicket(ticket=ticket, user=request.user.username, text=text, user_id=request.user.pk,
                                    type_user=type_user)
        answerticket.save(using='profile')
        return redirect('profile_detail_tickets', pk=pk)
    return render(request, 'front/Profile/profile_detail_tickets.html', context=context)
