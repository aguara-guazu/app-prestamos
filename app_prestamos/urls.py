from django.contrib import admin
from django.urls import path

from prestamos import views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('<str:transacion_id>', views.prestamo, name='prestamo'),
    path('admin/', views.admin, name='admin'),
    path('admin/<str:transacion_id>', views.edit_prestamo, name='edit_prestamo'),
]

handler404 = 'prestamos.views.err_page'
handler500 = 'prestamos.views.err_page'
