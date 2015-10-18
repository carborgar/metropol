# -*- coding: utf-8 -*-
import datetime

from django import forms
from chosen import forms as chosenforms
from django.forms import DateField

from .models import *
from metropol.validators import validate_past_date


# Custom form to set "required" attributes to HTML
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


# Custom fields
class PastDateField(DateField):
    default_validators = [validate_past_date]


class PersonForm(MetropolForm):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    name = forms.CharField(label='Nombre')
    id_number = forms.CharField(label='DNI/CIF', required=False)
    nationality = forms.CharField(label='Nacionalidad', required=False)
    email = forms.EmailField(label='Correo', required=False)
    web = forms.URLField(label='Página web', required=False, widget=forms.URLInput(attrs={'data-error': "Patrón: http://www.ejemplo.com"}));
    creation_date = PastDateField(label='Fecha de alta', initial=datetime.datetime.now)


class PersonListFilterForm(MetropolForm):
    role = forms.ChoiceField(required=False, label="Rol")
    keyword = forms.CharField(label='Criterio de búsqueda', required=False)

    def __init__(self, *args, **kwargs):
        super(PersonListFilterForm, self).__init__(*args, **kwargs)
        choices = [(role.id, role) for role in Role.objects.all()]
        choices.extend([('-1', 'Sin rol'), (None, 'Todos')])
        self.fields['role'].choices = sorted(choices, key=lambda tup: str(tup[1]))


class PhoneForm(MetropolForm):
    person_id = forms.IntegerField(widget=forms.HiddenInput())
    phone_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    phone_type = forms.ModelChoiceField(label="Tipo", queryset=PhoneType.objects.all(), empty_label='Selecciona un tipo')
    number = forms.CharField(label="Número")


class AddressForm(MetropolForm):
    person_id = forms.IntegerField(widget=forms.HiddenInput())
    address_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    address = forms.CharField(label="Dirección")
    location = forms.CharField(label="Población")
    zipcode = forms.CharField(label="Código postal", required=False)
    province = forms.CharField(label="Provincia", required=False)


class ExpedientForm(MetropolForm):
    # The queryset for persons (used 4 times)
    persons = Person.objects.all()
    user_types = UserType.objects.filter(is_active=True)

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    expedient_num = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'min': '1'}), label="Nº expediente")
    branch = forms.ModelChoiceField(queryset=LawBranch.objects.all(), label="Rama derecho", empty_label='Selecciona una rama')
    phase = forms.IntegerField(label="Fase", widget=forms.Select())
    state = forms.ModelChoiceField(queryset=State.objects.all(), label="Estado")
    headquarters = forms.ModelChoiceField(queryset=Headquarters.objects.all(), label="Sede")
    user_type = forms.ModelChoiceField(queryset=UserType.objects.filter(is_active=True), label="Tipo usuario")
    description = forms.CharField(widget=forms.Textarea(), required=False, label="Descripción")
    customers = chosenforms.ChosenModelMultipleChoiceField(queryset=persons, label="Clientes", overlay='Selecciona los clientes')
    contraries = chosenforms.ChosenModelMultipleChoiceField(queryset=persons, label="Contrarios", overlay='Selecciona los contrarios')
    contrary_lawyers = chosenforms.ChosenModelMultipleChoiceField(queryset=persons, label="Abogados contrarios", overlay='Selecciona los abogados contrarios')
    attorneys = chosenforms.ChosenModelMultipleChoiceField(required=False, queryset=persons, label="Procuradores", overlay='Selecciona los procuradores')
    creation_date = PastDateField(label="Fecha alta", initial=datetime.datetime.now)
    end_date = forms.DateField(label="Fecha cierre", required=False)

    def clean_expedient_number(self):
        is_creating = not self.cleaned_data['id']
        if is_creating:
            data = self.cleaned_data['expedient_num']
            # If the user is creating a new one, check that the expedient number does not exists
            if is_creating and Expedient.objects.filter(id=data).exists():
                raise forms.ValidationError("Este número de expediente ya existe.")

        return data

    def clean_phase(self):
        data = self.cleaned_data['phase']
        all_phases = [phase.id for phase in Phase.objects.all()]

        if data not in all_phases:
            raise forms.ValidationError("Esta fase no es válida.")

        return data

    def clean(self):
        cleaned_data = super(ExpedientForm, self).clean()
        form_creation_date = cleaned_data.get("creation_date")
        form_end_date = cleaned_data.get("end_date")
        form_state = cleaned_data.get("state")

        # Check that, when the state is CERRADO, the field end_date is mandatory. Else must be null
        if form_state.text_help == "CERRADO":
            if not form_end_date:
                raise forms.ValidationError("Debes seleccionar una fecha de cierre.")
        else:
            self.cleaned_data['end_date'] = None

        if form_end_date:
            # Check that creation date is before or equal to end date
            if form_creation_date > form_end_date:
                raise forms.ValidationError("La fecha de cierre debe ser igual o posterior a la fecha de alta.")

