from metropol_abogados.models import Person
from metropol_abogados.utils import DateUtils


def save_from_form(person_form):
    person = Person()
    # If id is present, get the DB person and edit
    person_id = person_form.cleaned_data['id']

    if person_id:
        person = Person.objects.get(id=person_id)

    person.name = person_form.cleaned_data['name']
    person.id_number = person_form.cleaned_data['id_number']
    person.email = person_form.cleaned_data['email']
    person.web = person_form.cleaned_data['web']
    person.nationality = person_form.cleaned_data['nationality']

    # Set the creation date -> we need to convert it into a datetime
    form_creation_date = person_form.cleaned_data['creation_date']
    person.creation_date = DateUtils.convert_date_to_datetime(form_creation_date)

    person.save()


def find_all():
    result = Person.objects.all()

    return result


def build_initial_data(person):
    return {'id': person.id, 'name': person.name, 'id_number': person.id_number, 'email': person.email,
            'web': person.web, 'nationality': person.nationality, 'creation_date': person.creation_date}
