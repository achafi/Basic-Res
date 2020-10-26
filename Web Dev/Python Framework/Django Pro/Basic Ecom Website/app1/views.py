from math import ceil

from django.shortcuts import render
from .models import Product


# Create your views here.
def index(request):
    product=Product.objects.all()
    nSlides=len(product)//4 +ceil((len(product)/4)-(len(product)//4))
    dic = {'no_of_slides':nSlides,'range':range(1,nSlides),'products': product}
    return render(request,'app1/index.html', dic)

def about(request):
    return render(request,'app1/about.html')

def contact(request):
    return render(request,'app1/index.html')

def tracker(request):
    return render(request,'app1/index.html')

def xyz(request):
    return render(request,'app1/index.html')