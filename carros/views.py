from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Carro

def lista_carros(request):
    if request.method == 'POST':
        if 'cadastrar' in request.POST:
            placa = request.POST.get('placa', '').upper().strip()
            if not Carro.objects.filter(placa=placa).exists():
                Carro.objects.create(
                    placa=placa, cor=request.POST.get('cor'), 
                    escritorio=request.POST.get('escritorio'), 
                    status='pre_localizado'
                )
                messages.success(request, f"Veículo {placa} cadastrado!")
        elif 'proxima_fase' in request.POST:
            c = get_object_or_404(Carro, id=request.POST.get('carro_id'))
            c.status = 'localizado' if c.status == 'pre_localizado' else 'apreendido'
            c.save()
        elif 'excluir' in request.POST:
            Carro.objects.filter(id=request.POST.get('carro_id')).delete()
        return redirect('lista_carros')
    return render(request, 'carros/lista.html', {'carros': Carro.objects.all()})


