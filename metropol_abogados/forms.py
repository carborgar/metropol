# -*- coding: utf-8 -*-
import datetime

from django import forms
from chosen import forms as chosenforms
from django.forms import DateField
from bootstrap3_datetime.widgets import DateTimePicker

from .utils import FormUtils
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
    web = forms.URLField(label='Página web', required=False,
                         widget=forms.URLInput(attrs={'data-error': "Patrón: http://www.ejemplo.com"}))
    creation_date = PastDateField(label='Fecha de alta', initial=datetime.datetime.now,
                                  widget=DateTimePicker(options={"format": "DD/MM/YYYY", "pickTime": False},
                                               attrs={'placeholder': 'DD/MM/AAAA'}))


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
    phone_type = forms.ModelChoiceField(label="Tipo", queryset=PhoneType.objects.all())
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
    user_types = Attendant.objects.filter(is_active=True)

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    expedient_num = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'min': '1'}), label="Nº expediente")
    branch = forms.ModelChoiceField(queryset=LawBranch.objects.all(), required=False, label="Rama derecho")
    phase = forms.IntegerField(label="Fase", required=False, widget=forms.Select())
    state = forms.ModelChoiceField(queryset=State.objects.all(), label="Estado")
    headquarters = forms.ModelChoiceField(queryset=Headquarters.objects.all(),required=False, label="Sede")
    attendant = forms.ModelChoiceField(queryset=Attendant.objects.filter(is_active=True), label="Encargado")
    description = forms.CharField(widget=forms.Textarea(), required=False, label="Asunto")
    customers = chosenforms.ChosenModelMultipleChoiceField(queryset=persons, label="Clientes", overlay='Clientes')
    contraries = chosenforms.ChosenModelMultipleChoiceField(queryset=persons, label="Contrarios", overlay='Contrarios')
    contrary_lawyers = chosenforms.ChosenModelMultipleChoiceField(queryset=persons, required=False, label="Abogados contrarios", overlay='Selecciona los abogados contrarios')
    own_attorneys = chosenforms.ChosenModelMultipleChoiceField(required=False, queryset=persons, label="Procuradores propios", overlay='Selecciona los procuradores propios')
    attorneys = chosenforms.ChosenModelMultipleChoiceField(required=False, queryset=persons, label="Procuradores contrarios", overlay='Selecciona los procuradores contrarios')
    creation_date = PastDateField(label="Fecha alta", initial=datetime.datetime.now,
                                  widget=DateTimePicker(options={"format": "DD/MM/YYYY", "pickTime": False},
                                               attrs={'placeholder': 'DD/MM/AAAA'}))
    end_date = forms.DateField(label="Fecha cierre", required=False, initial=datetime.datetime.now,
                                  widget=DateTimePicker(options={"format": "DD/MM/YYYY", "pickTime": False},
                                               attrs={'placeholder': 'DD/MM/AAAA'}))

    def clean_expedient_num(self):
        data = self.cleaned_data['expedient_num']
        is_creating = not self.cleaned_data['id']
        if is_creating and Expedient.objects.filter(id=data).exists():
            # If the user is creating a new one, check that the expedient number does not exists
            raise forms.ValidationError("Este número de expediente ya existe.")

        return data

    def clean_phase(self):
        data = self.cleaned_data['phase']
        all_phases = [phase.id for phase in Phase.objects.all()]

        if data and data not in all_phases:
            raise forms.ValidationError("Esta fase no es válida.")

        return data

    def clean(self):
        cleaned_data = super(ExpedientForm, self).clean()
        form_creation_date = cleaned_data.get("creation_date")
        form_end_date = cleaned_data.get("end_date")
        form_state = cleaned_data.get("state")
        selected_law_branch = cleaned_data.get("branch")
        selected_phase = cleaned_data.get("phase")

        # Check that, when the state is CERRADO, the field end_date is mandatory. Else must be null
        if form_state.text_help == "CERRADO":
            if not form_end_date:
                raise forms.ValidationError("Debes seleccionar una fecha de cierre.")
        else:
            self.cleaned_data['end_date'] = None

        # If there is a law branch selected, the field "phase" is mandatory
        if selected_law_branch and not selected_phase:
            raise forms.ValidationError("Si seleccionas una rama, debes seleccionar una fase.")

        if form_end_date and form_creation_date > form_end_date:
            # Check that creation date is before or equal to end date
            raise forms.ValidationError("La fecha de cierre debe ser igual o posterior a la fecha de alta.")


class ExpedientListFilterForm(MetropolForm):
    branch = forms.ChoiceField(label="Rama", required=False)
    headquarters = forms.ChoiceField(label="Sede", required=False)
    state = forms.ModelChoiceField(queryset=State.objects.all(), label="Estado", required=False)
    customers = chosenforms.ChosenModelMultipleChoiceField(queryset=Person.objects.all(), overlay="Clientes", required=False)
    keyword = forms.CharField(label='Criterio de búsqueda', required=False)

    def __init__(self, *args, **kwargs):
        super(ExpedientListFilterForm, self).__init__(*args, **kwargs)
        extra_choices = [('-1', 'Ninguna'), (None, 'Todos')]
        branch_choices = FormUtils.add_extra_choices([(b.id, b) for b in LawBranch.objects.all()], extra_choices)
        headquarters_choices = FormUtils.add_extra_choices([(h.id, h) for h in Headquarters.objects.all()], extra_choices)

        self.fields['branch'].choices = FormUtils.get_sorted_choices(branch_choices)
        self.fields['headquarters'].choices = FormUtils.get_sorted_choices(headquarters_choices)


class NoteForm(MetropolForm):
    note = forms.ModelChoiceField(queryset=Note.objects.all(), required=False)
    person = forms.ModelChoiceField(queryset=Person.objects.all(), required=False)
    expedient = forms.ModelChoiceField(queryset=Expedient.objects.all(), required=False)
    description = forms.CharField()


class ExpirationForm(MetropolForm):
    expiration = forms.ModelChoiceField(queryset=Expiration.objects.all(), required=False, widget=forms.HiddenInput())
    expedient = forms.ModelChoiceField(queryset=Expedient.objects.all(), widget=forms.HiddenInput())
    date = forms.DateTimeField(label="Fecha",
                               widget=DateTimePicker(options={"format": "DD/MM/YYYY HH:mm", "pickSeconds": False},
                                                     attrs={'placeholder': 'DD/MM/AAAA HH:mm'}))
    place = forms.CharField(label="Lugar", required=False)
    description = forms.CharField(widget=forms.Textarea(), required=False, label="Asunto")
    event = forms.ModelChoiceField(queryset=Event.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        expedient_events = kwargs.pop("available_events")
        super(ExpirationForm, self).__init__(*args, **kwargs)

        # If the expedient has branch, take the events related to the branch
        if expedient_events:
            self.fields["event"].queryset = expedient_events

        else:
            # Otherwise, hide the input
            self.fields['event'].widget = forms.HiddenInput()


class BudgetForm(MetropolForm):
    YES_NO = ((True, 'Sí'), (False, 'No'))
    state_budget = forms.ModelChoiceField(queryset=StateBudget.objects.all(), label="Estado", required=False)
    amount = forms.DecimalField(label="Cantidad total")
    own_attorney = forms.BooleanField(required=False, label="Procurador propio", widget=forms.Select(choices=YES_NO))
    description = forms.CharField(widget=forms.Textarea(), required=False, label="Descripción")


class PaymentForm(MetropolForm):
    amount = forms.DecimalField(label="Cantidad entregada")
    date = PastDateField(label='Fecha', initial=datetime.datetime.now,
                         widget=DateTimePicker(options={"format": "DD/MM/YYYY", "pickTime": False},
                                               attrs={'placeholder': 'DD/MM/AAAA'}))

