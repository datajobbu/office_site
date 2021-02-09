from django.shortcuts import render
from django.db.models import F, Sum
from .models import Signoff
# Create your views here.
def index(request):
    requests = Signoff.objects.order_by('-request_date', '-id').values()
    context = {
        'requests': requests,
    }
    return render(request, 'request_list.html', context)


def signoff(request):
    signs = Signoff.objects.values('request_date')
    
    date_list = []
    for sign in signs:
        date_list.append(sign['request_date'].strftime("%Y-%m-%d"))
    unq_date = sorted(set(date_list), reverse=True)
    

    context = {
        "date_list": unq_date,
    }

    return render(request, 'signoff_list.html', context)


def detail(request, date):
    annot = Signoff.objects.annotate(total=F('unit') * F('qnt'))
    requests = annot.filter(request_date=date).values()
    total = requests.aggregate(Sum(F('total')))
    
    context = {
        'requests': requests,
        'date': date,
        'total': total,
    }
    
    return render(request, 'request_pdf.html', context)
