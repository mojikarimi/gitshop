from __future__ import unicode_literals
import datetime
from django.shortcuts import render
from jdatetime import datetime
from Main.models import Visit
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def panel_index(request, month):
    if month == '':
        # If the month was empty, it will be replaced by the current month
        month = str(datetime.now().month)
        if len(month) == 1:
            # If the month is a single digit, a zero is added behind it
            month = '0' + f'{month}'  # '1' => '01'
        request.path += month
    else:
        month = month
    year = datetime.now().year
    datas = Visit.objects.filter(x__startswith=f'{year}-{month}').order_by('x')  # Filters data based on month and year
    website_visit_data = []
    '''=> [ {'x':date(0,1,2....,30|31),'y':count visit ,'IndexLabel': count visit},
    {'x':date(0,1,2....,30|31),'y':count visit ,'IndexLabel': count visit},... ] '''
    for data in datas:
        website_visit_data.append(
            {'x': int(data.x[-2:]), 'y': data.y,
             'indexLabel': str(data.y)})  # x: date(1,2,3,...,30|31) y:count visit IndexLabel:count visit
    context = {'website_visit_data': website_visit_data}
    return render(request, 'back/PanelPanel/panel_index.html', context=context)
