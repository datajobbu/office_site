from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import F, Sum
from django.urls import reverse
from .models import Signoff
from .forms import SignoffForm


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

@login_required(login_url='login')
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

@login_required(login_url='login')
def request_create(request):
    form = SignoffForm()

    if request.method == 'POST':
        form = SignoffForm(request.POST)

        if form.is_valid():
            request = form.save(commit=False)
            request.save()
            return redirect(reverse('list'))
        
        else:
            form = SignoffForm()
    
    context = {
        'form': form
    }

    return render(request, 'request_form.html', context)


def login(request):
    return render(request, 'login.html')