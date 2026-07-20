from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from usuarios.decorators import admin_required
from .forms import EmpresaForm
from .models import Empresa


@login_required
def empresa_list(request):
    empresas = Empresa.objects.all()
    return render(request, 'empresas/empresa_list.html', {'empresas': empresas})


@admin_required
def empresa_create(request):
    form = EmpresaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        empresa = form.save()
        messages.success(request, f'Empresa {empresa.razon_social} registrada correctamente.')
        return redirect('empresa_list')
    return render(request, 'empresas/empresa_form.html', {'form': form})
