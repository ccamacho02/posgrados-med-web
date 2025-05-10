from django.shortcuts import render

# Create your views here.
def lista_programas(request):
    return render(request, 'lista_programas.html')