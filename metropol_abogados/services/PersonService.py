__author__ = 'Carlos'

from metropol_abogados.models import Person


def save_from_form(person_form):
    person = Person()

    person.name = person_form.cleaned_data['name']
    person.id_number = person_form.cleaned_data['id_number']
    person.email = person_form.cleaned_data['nationality']
    person.web = person_form.cleaned_data['email']
    person.nationality = person_form.cleaned_data['website']
    person.creation_date = person_form.cleaned_data['creation_date']

    person.save()


def find_all():
    result = Person.objects.all()

    return result
