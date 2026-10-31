from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
from .models import Equipo

# Lista de comunas de la Provincia de Santiago (puedes agregar o quitar según prefieras)
COMUNAS_SANTIAGO = [
    ('', 'Seleccione su comuna...'),
    ('Cerrillos', 'Cerrillos'),
    ('Cerro Navia', 'Cerro Navia'),
    ('Conchalí', 'Conchalí'),
    ('El Bosque', 'El Bosque'),
    ('Estación Central', 'Estación Central'),
    ('Huechuraba', 'Huechuraba'),
    ('Independencia', 'Independencia'),
    ('La Cisterna', 'La Cisterna'),
    ('La Florida', 'La Florida'),
    ('La Granja', 'La Granja'),
    ('La Pintana', 'La Pintana'),
    ('La Reina', 'La Reina'),
    ('Las Condes', 'Las Condes'),
    ('Lo Barnechea', 'Lo Barnechea'),
    ('Lo Espejo', 'Lo Espejo'),
    ('Lo Prado', 'Lo Prado'),
    ('Macul', 'Macul'),
    ('Maipú', 'Maipú'),
    ('Ñuñoa', 'Ñuñoa'),
    ('Pedro Aguirre Cerda', 'Pedro Aguirre Cerda'),
    ('Peñalolén', 'Peñalolén'),
    ('Providencia', 'Providencia'),
    ('Pudahuel', 'Pudahuel'),
    ('Quilicura', 'Quilicura'),
    ('Quinta Normal', 'Quinta Normal'),
    ('Recoleta', 'Recoleta'),
    ('Renca', 'Renca'),
    ('San Joaquín', 'San Joaquín'),
    ('San Miguel', 'San Miguel'),
    ('San Ramón', 'San Ramón'),
    ('Santiago', 'Santiago'),
    ('Vitacura', 'Vitacura'),
    ('Puente Alto', 'Puente Alto'),
    ('San Bernardo', 'San Bernardo'),
]

class RegistroCapitanForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        label="Correo Electrónico",
        error_messages={'invalid': 'Por favor, introduce un correo electrónico válido (ej: usuario@dominio.com).'}
    )
    
    telefono = forms.CharField(
        max_length=15, 
        required=True, 
        label="Teléfono de Contacto (Ej: +56912345678 o 912345678)",
        help_text="Número chileno de 9 dígitos o formato internacional."
    )
    
    comuna = forms.ChoiceField(
        choices=COMUNAS_SANTIAGO, 
        required=True, 
        label="Comuna (Santiago)"
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        # Expresión regular que acepta formato chileno con o sin +569 y 8 o 9 dígitos
        patron = r'^(\+?56)?(\s?9)(\s?\d){8}$'
        
        # Limpiamos espacios para la validación interna
        telefono_limpio = telefono.replace(" ", "")
        
        if not re.match(r'^\+?[0-9]{8,15}$', telefono_limpio):
            raise forms.ValidationError("El número de teléfono no es válido. Debe tener un formato numérico correcto (Ej: +56912345678).")
        return telefono

class CrearEquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre']
        labels = {'nombre': 'Nombre del Equipo'}