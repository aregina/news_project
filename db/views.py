from django.shortcuts import render
from db.models import *

# Create your views here.


def index(request):

    context = {"key": KeyWord.objects.get(word="путин")}
    return render(request, 'db/index.html', context)
