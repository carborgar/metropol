__author__ = 'Carlos'
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from metropol_abogados.services import AddressService
from metropol_abogados.models import Address, Person
from metropol_abogados.forms import AddressForm
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect


def edit(request, person_id, address_id=None):
    person = get_object_or_404(Person, id=person_id)
    initial_data = {'person_id': person.id}

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            AddressService.save_from_form(form, person)
            msg = "Dirección %s correctamente" % ("guardada" if not address_id else "editada")
            messages.success(request, msg)

            return HttpResponseRedirect(reverse('person-details', args=(person_id,)))
    else:
        if address_id:
            phone = get_object_or_404(Address, id=address_id)
            additional_data = AddressService.build_additional_data(phone)
            initial_data.update(additional_data)

        form = AddressForm(initial=initial_data)

    return render_to_response("address/edit.html", {'form': form}, context_instance=RequestContext(request))


def delete(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    person_id = address.person.id
    address.delete()
    messages.success(request, "Se ha borrado la dirección correctamente.")

    return HttpResponseRedirect(reverse('person-details', args=(person_id,)))
