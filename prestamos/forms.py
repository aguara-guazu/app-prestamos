from django import forms
from django.forms import ModelForm

from .models import Prestamo


class PrestamoForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(label='Apellido', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dni = forms.IntegerField(label='DNI', max_value=99999999, min_value=1000000, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    genero = forms.ChoiceField(label='Genero', choices=(('M', 'Masculino'), ('F', 'Femenino'), ('X', 'No binario')),
                               widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    monto = forms.DecimalField(label='Monto', max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class EditPrestamoForm(ModelForm):
    class Meta:
        model = Prestamo
        fields = '__all__'
        exclude = ['cliente']

    cliente_nombre = forms.CharField(label='Cliente', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     disabled=True)
    dni = forms.IntegerField(label='DNI', max_value=99999999, min_value=1000000, widget=forms.TextInput(attrs={'class':
                                                                                                                   'form-control'}),
                             disabled=True)
    fecha_solicitud = forms.DateField(label='Fecha Solicitud', widget=forms.DateInput(attrs={'type': 'date', 'class':
        'form-control'}))
    monto = forms.DecimalField(label='Monto', max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    estado = forms.ChoiceField(label='Estado', choices=(('A', 'Aprobado'), ('R', 'Rechazado')),
                               widget=forms.Select(attrs={'class': 'form-control'}))
    transacion_id = forms.CharField(label='Transacion ID', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                    disabled=True)

    field_order = ['cliente_nombre', 'dni', 'fecha_solicitud', 'monto', 'estado', 'transacion_id']
