# alumnos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('alumnos/', views.listar_alumnos, name='listar_alumnos'),
    path('nuevo/', views.crear_alumno, name='crear_alumno'),
    path('editar/<int:pk>/', views.editar_alumno, name='editar_alumno'),
    path('eliminar/<int:pk>/', views.eliminar_alumno, name='eliminar_alumno'),

    #escaner
    path('', views.escaneo_qr, name='escaneo_qr'),
    path('registrar-ingreso/', views.registrar_ingreso, name='registrar_ingreso'),

    #Listado de ingresos
     path('ingresos/', views.lista_ingresos, name='lista_ingresos'),
]
