from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import F, Sum
from django.urls import reverse
from .models import Signoff
from .forms import SignoffForm


@login_required(login_url='/login/')
def index(request):
    """ 구매 등록 리스트 """
    requests = Signoff.objects.order_by('-request_date', '-id').values()
    context = {
        'requests': requests,
    }
    return render(request, 'signoff/request_list.html', context)


@login_required(login_url='/login/')
def signoff(request):
    """ 결재 리스트 """
    """ SQL로 Unique 처리하기 """
    signs = Signoff.objects.values('request_date')
    
    date_list = []
    for sign in signs:
        date_list.append(sign['request_date'].strftime("%Y-%m-%d"))
    unq_date = sorted(set(date_list), reverse=True)

    context = {
        "date_list": unq_date,
    }

    return render(request, 'signoff/signoff_list.html', context)


@login_required(login_url='/login/')
def detail(request, date):
    """ 보고서 생성 및 결재 서명 """
    """ 요청 다음 날 결재되도록 처리 """
    annot = Signoff.objects.annotate(total=F('unit') * F('qnt'))
    requests = annot.filter(request_date=date).values()
    total = requests.aggregate(Sum(F('total')))
    
    context = {
        'requests': requests,
        'date': date,
        'total': total,
    }
    
    return render(request, 'signoff/request_pdf.html', context)


@login_required(login_url='/login/')
def request_create(request):
    form = SignoffForm()

    if request.method == 'POST':
        form = SignoffForm(request.POST)

        if form.is_valid():
            request = form.save(commit=False)
            request.save()
            return redirect(reverse('signoff:list'))
        
        else:
            form = SignoffForm()
    
    context = {
        'form': form
    }

    return render(request, 'signoff/request_form.html', context)