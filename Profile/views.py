from __future__ import unicode_literals

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
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def profile_dashboard(request):
    if request.method == 'POST':
        x = ''.join((random.choice('0123456789') for i in range(5)))  # Creating a verification code
        request.session['username'] = request.user.username
        user = CustomUser.objects.get(pk=request.user.pk)
        user.verify_code = x
        user.save()
        send_mail(subject='moji', message=f'hi moji {x}', from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[request.user.email])  # Send email
        return redirect('verify_email')
    return render(request, 'front/Profile/profile_dashboard.html')


@login_required
def profile_tickets(request):
    if not request.user.is_active:  # Account activation notification
        messages.warning(request, 'Please activate your account')
        return redirect('profile_dashboard')
    parts = Group.objects.using('profile').all()
    tickets = Tickets.objects.using('profile').order_by('-date').filter(user_id=request.user.pk)
    for i in tickets.filter(status='درحال بررسی'):

        if ((int(datetime.now().year) * 365) + (int(datetime.now().month) * 30) + (int(datetime.now().day))) - (
                (int(i.date[:4]) * 365) + (int(i.date[5:7]) * 30) + (int(i.date[8:10]))) >= 10:
            i.status = 'بسته شده'
            i.save(using='profile')
    context = {'parts': parts, 'tickets': tickets}
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
    ticket = Tickets.objects.using('profile').get(pk=pk, user_id=request.user.pk)
    answertickets = AnswerTicket.objects.using('profile').order_by('-date').filter(ticket=ticket)
    context = {'ticket': ticket, 'answertickets': answertickets, 'number': len(answertickets)}
    if request.method == 'POST':
        text = request.POST.get('text')
        type_user = request.POST.get('type_user')
        answerticket = AnswerTicket(ticket=ticket, user=request.user.username, text=text, user_id=request.user.pk,
                                    type_user=type_user)
        answerticket.save(using='profile')
        return redirect('profile_detail_tickets', pk=pk)
    return render(request, 'front/Profile/profile_detail_tickets.html', context=context)
