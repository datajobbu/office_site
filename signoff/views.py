from django.shortcuts import render
from .models import Signoff
# Create your views here.
def index(request):
    requests = Signoff.objects.order_by('id').values()
    context = {
        'requests': requests,
    }
    return render(request, 'request_list.html', context)