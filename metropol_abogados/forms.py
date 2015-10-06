__author__ = 'Carlos'
# -*- coding: utf-8 -*-
from django import forms
import datetime
from metropol_abogados.models import Role, PhoneType


class MetropolForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MetropolForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})
            if field.required:
                field.widget.attrs.update({'required': 'required'})


class PersonForm(MetropolForm):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    name = forms.CharField(label='Nombre')
    id_number = forms.CharField(label='DNI/CIF', required=False)
    nationality = forms.CharField(label='Nacionalidad', required=False)
    email = forms.EmailField(label='Correo', required=False)
    web = forms.URLField(label='Página web', required=False, widget=forms.URLInput(attrs={'data-error': "Patrón: http://www.ejemplo.com"}));
    creation_date = forms.DateField(label='Fecha de alta', initial=datetime.datetime.now)

    def clean_creation_date(self):
        form_creation_date = self.cleaned_data['creation_date']
        today = datetime.date.today()

        if form_creation_date > today:
            raise forms.ValidationError('La fecha no puede ser en el futuro.')

        return form_creation_date


class PersonListFilterForm(MetropolForm):
    role = forms.ChoiceField(required=False, label="Rol")
    keyword = forms.CharField(label='Nombre', required=False)

    def __init__(self, *args, **kwargs):
        super(PersonListFilterForm, self).__init__(*args, **kwargs)
        choices = [(role.id, role) for role in Role.objects.all()]
        choices.extend([('-1', 'Sin rol'), (None, 'Todos')])
        self.fields['role'].choices = sorted(choices, key=lambda tup: str(tup[1]))


class PhoneForm(MetropolForm):
    person_id = forms.IntegerField(widget=forms.HiddenInput())
    phone_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    phone_type = forms.ModelChoiceField(label="Tipo", queryset=PhoneType.objects.all())
    number = forms.CharField(label="Número")


class AddressForm(MetropolForm):
    person_id = forms.IntegerField(widget=forms.HiddenInput())
    address_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    address = forms.CharField(label="Dirección")
    location = forms.CharField(label="Población")
    zipcode = forms.CharField(label="Código postal", required=False)
    province = forms.CharField(label="Provincia", required=False)
