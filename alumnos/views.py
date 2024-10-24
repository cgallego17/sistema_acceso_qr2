# alumnos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AlumnoForm
from django.http import JsonResponse
from .models import Alumno, RegistroIngreso
from django.views.decorators.csrf import csrf_exempt

# Listar alumnos
def listar_alumnos(request):
    alumnos = Alumno.objects.all()
    return render(request, 'alumnos/lista.html', {'alumnos': alumnos})

# Crear un nuevo alumno
def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_alumnos')
    else:
        form = AlumnoForm()
    return render(request, 'alumnos/formulario.html', {'form': form})

# Editar un alumno
def editar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            return redirect('listar_alumnos')
    else:
        form = AlumnoForm(instance=alumno)
    return render(request, 'alumnos/formulario.html', {'form': form})

# Eliminar un alumno
def eliminar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == 'POST':
        alumno.delete()
        return redirect('listar_alumnos')
    return render(request, 'alumnos/confirmar_eliminar.html', {'alumno': alumno})

@csrf_exempt
def registrar_ingreso(request):
    if request.method == 'POST':
        codigo_qr = request.POST.get('qr_code')
        if codigo_qr:
            # Suponiendo que el código QR está en formato 'ID-Nombre'
            try:
                alumno_id = codigo_qr.split('-')[0]  # Obtén solo el ID
                alumno = Alumno.objects.get(id=int(alumno_id))  # Convierte a entero
                RegistroIngreso.objects.create(alumno=alumno)
                return JsonResponse({'success': True, 'message': 'Ingreso registrado con éxito.'})
            except Alumno.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Alumno no encontrado.'})
            except ValueError:
                return JsonResponse({'success': False, 'message': 'ID inválido proporcionado.'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
        else:
            return JsonResponse({'success': False, 'message': 'Código QR no proporcionado.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


#Scaneo Qr
def escaneo_qr(request):
    return render(request, 'scanner/escaneo_qr.html')


#Listado de ingresos
def lista_ingresos(request):
    registros = RegistroIngreso.objects.all().order_by('-hora_ingreso')  # Ordenar por fecha y hora
    return render(request, 'ingresos/lista.html', {'registros': registros})