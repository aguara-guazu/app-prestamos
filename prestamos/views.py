from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import SuspiciousOperation
from django.core.exceptions import ValidationError
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.safestring import mark_safe

from .forms import EditPrestamoForm
from .forms import PrestamoForm
from .models import Cliente
from .models import Prestamo
from .utils import pre_aprobado


def err_page(request, exception=None):
    if not exception:
        exception = 'El prestamo que buscabas no existe'

    if request.method == 'POST':

        if request.POST.get('buscar'):
            prestamo = request.POST.get('transacion_id')
            if prestamo:
                return redirect('prestamo', transacion_id=prestamo)

    return render(request, '404.html', {'mensaje': exception})


def index(request):
    if request.method == 'POST':

        if request.POST.get('buscar'):
            prestamo = request.POST.get('transacion_id')
            if prestamo:
                return redirect('prestamo', transacion_id=prestamo)
            else:
                return HttpResponseNotFound(err_page(request, 'El prestamo buscado es invalido'))
        else:
            form = PrestamoForm(request.POST)
            if form.is_valid():
                try:
                    cliente = Cliente.objects.get(dni=form.cleaned_data['dni'], genero=form.cleaned_data['genero'])
                except Cliente.DoesNotExist:
                    cliente = Cliente(dni=form.cleaned_data['dni'],
                                      nombre=form.cleaned_data['nombre'],
                                      apellido=form.cleaned_data['apellido'],
                                      genero=form.cleaned_data['genero'],
                                      email=form.cleaned_data['email'])
                    cliente.save()
                try:
                    estado = pre_aprobado(cliente.dni)
                    prestamo = Prestamo(cliente=cliente, monto=form.cleaned_data['monto'], estado=estado)
                    prestamo.save()
                except SuspiciousOperation as e:
                    return HttpResponseNotFound(err_page(request, 'No pudimos procesar tu operación,  intenta de nuevo más tarde'))

                mensaje = f'Tu solicitud de prestamo ha sido evaluada con exito y este fue <strong> {prestamo.get_estado_display()} ' \
                          f'</strong>' \
                          f'<br/>Tu numero de transaccion es: <strong> {prestamo.transacion_id} </strong>'
                messages.success(request, mark_safe(mensaje))
            else:
                messages.error(request, 'El formulario contiene errores, por favor corrijalos')
    form = PrestamoForm()
    return render(request, 'index.html', {'form': form})


def prestamo(request, transacion_id: str):
    try:
        prestamo = Prestamo.objects.get(transacion_id=transacion_id)
        return render(request, 'prestamos.html', {'prestamo': prestamo})
    except ValidationError as e:
        return HttpResponseNotFound(err_page(request, 'El prestamo buscado no tiene formato valido'))
    except Prestamo.DoesNotExist:
        return HttpResponseNotFound(err_page(request, 'El prestamo buscado no existe'))


@staff_member_required
def admin(request):
    prestamos = Prestamo.objects.all()

    if request.method == 'POST':
        prestamo = request.POST.get('transacion_id')
        if request.POST.get('editar'):
            return redirect('edit_prestamo', transacion_id=prestamo)
        elif request.POST.get('eliminar'):
            prestamos.get(transacion_id=prestamo).delete()
    return render(request, 'prestamo_admin.html', {'prestamos': prestamos})


@staff_member_required
def edit_prestamo(request, transacion_id: str):
    prestamo = get_object_or_404(Prestamo, transacion_id=transacion_id)

    initial = {'dni': prestamo.cliente.dni,
               'cliente_nombre': prestamo.cliente.__str__(),
               'transacion_id': prestamo.transacion_id,
               }

    if request.method == 'POST':
        if request.POST.get('cancelar'):
            return redirect('admin')
        else:
            form = EditPrestamoForm(request.POST, instance=prestamo, initial=initial)
            if form.is_valid():
                form.save()
                messages.success(request, 'El prestamo ha sido modificado con exito')
            else:
                messages.error(request, 'El prestamo no ha sido modificado, alguno de los datos es invalido')
    else:
        form = EditPrestamoForm(instance=prestamo, initial=initial)
    return render(request, 'edit_prestamo.html', {'form': form, 'prestamo': prestamo})
