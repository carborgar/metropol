__author__ = 'Carlos'

from metropol_abogados.models import Phone


def save_from_form(phone_form, person):
    phone = Phone()
    # If id is present, get the DB person and edit
    phone_id = phone_form.cleaned_data['phone_id']

    if phone_id:
        phone = Phone.objects.get(id=phone_id)

    phone.number = phone_form.cleaned_data['number']
    phone.phone_type = phone_form.cleaned_data['phone_type']
    phone.person = person

    phone.save()


def build_additional_data(phone):
    return {'phone_id': phone.id, 'number': phone.number, 'phone_type': phone.phone_type}
