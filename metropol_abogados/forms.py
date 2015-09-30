__author__ = 'Carlos'
from django import forms
import datetime
from metropol_abogados.models import Person, Role
from django.utils.translation import ugettext as _


class MetropolForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MetropolForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})


class PersonForm(MetropolForm):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput(attrs={'required': 'required'}))
    id_number = forms.CharField(label=_('id.number'), required=False)
    nationality = forms.CharField(label=_('Nationality'), required=False)
    email = forms.EmailField(label=_('Email'), required=False)
    website = forms.URLField(label=_('Web'), required=False, widget=forms.URLInput(attrs={'data-error': _('url.pattern.help')}));
    creation_date = forms.DateField(label=_('creation.date'), initial=datetime.date.today, widget=forms.DateInput(attrs={'required': 'required'}))

    def clean_creation_date(self):
        form_creation_date = self.cleaned_data['creation_date']
        today = datetime.date.today()

        if form_creation_date > today:
            raise forms.ValidationError(_('error.date.must.be.future'))


class PersonListFilterForm(MetropolForm):
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=False, empty_label=_("Todos"))
    keyword = forms.CharField(label=_('Keyword'), required=False, widget=forms.TextInput())
