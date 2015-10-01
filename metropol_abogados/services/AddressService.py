__author__ = 'Carlos'

from metropol_abogados.models import Address


def save_from_form(address_form, person):
    address = Address()
    # If id is present, get the DB person and edit
    address_id = address_form.cleaned_data['address_id']

    if address_id:
        address = Address.objects.get(id=address_id)

    address.address = address_form.cleaned_data['address']
    address.location = address_form.cleaned_data['location']
    address.postal_code = address_form.cleaned_data['zipcode']
    address.province = address_form.cleaned_data['province']
    address.person = person

    address.save()


def build_additional_data(address):
    return {'address_id': address.id, 'address': address.address, 'location': address.location,
            'zipcode': address.postal_code, 'province': address.province}
