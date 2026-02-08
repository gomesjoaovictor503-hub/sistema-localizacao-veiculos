from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Carro

def lista_carros(request):
    # 1. Tenta pegar o nome do usuário que está salvo na "sessão" do navegador
    usuario_logado = request.session.get('usuario_nome')

    if request.method == 'POST':
        # Lógica para definir o nome de acesso (Login simples)
        if 'definir_usuario' in request.POST:
            nome = request.POST.get('nome_acesso', '').strip()
            if nome:
                request.session['usuario_nome'] = nome
                return redirect('lista_carros')

        # Se o usuário não estiver identificado, ele não pode cadastrar nem ver nada
        if not usuario_logado:
            return redirect('lista_carros')

        if 'cadastrar' in request.POST:
            placa = request.POST.get('placa', '').upper().strip()
            if not Carro.objects.filter(placa=placa).exists():
                Carro.objects.create(
                    placa=placa, 
                    cor=request.POST.get('cor'), 
                    escritorio=request.POST.get('escritorio'), 
                    status='pre_localizado',
                    usuario_acesso=usuario_logado  # Salva o nome de quem cadastrou
                )
                messages.success(request, f"Veículo {placa} cadastrado em sua conta!")
        
        elif 'proxima_fase' in request.POST:
            # Garante que o usuário só altere carros que pertencem a ele
            c = get_object_or_404(Carro, id=request.POST.get('carro_id'), usuario_acesso=usuario_logado)
            c.status = 'localizado' if c.status == 'pre_localizado' else 'apreendido'
            c.save()
            
        elif 'excluir' in request.POST:
            # Garante que o usuário só exclua carros que pertencem a ele
            Carro.objects.filter(id=request.POST.get('carro_id'), usuario_acesso=usuario_logado).delete()
            
        elif 'sair' in request.POST:
            # Limpa a sessão para trocar de usuário
            request.session.flush()
            return redirect('lista_carros')

        return redirect('lista_carros')

    # 2. Filtra os carros: só aparecem os que têm o nome do usuário logado
    carros_do_usuario = Carro.objects.filter(usuario_acesso=usuario_logado) if usuario_logado else []

    return render(request, 'carros/lista.html', {
        'carros': carros_do_usuario,
        'usuario_logado': usuario_logado
    })


