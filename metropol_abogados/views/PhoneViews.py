# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from metropol_abogados.services import PhoneService
from metropol_abogados.models import Phone, Person
from metropol_abogados.forms import PhoneForm
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required


@permission_required('auth.management_metropol')
def edit(request, person_id, phone_id=None):
    person = get_object_or_404(Person, id=person_id)
    initial_data = {'person_id': person.id}

    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            PhoneService.save_from_form(form, person)
            msg = "Teléfono %s correctamente" % ("guardado" if not phone_id else "editado")
            messages.success(request, msg)

            return HttpResponseRedirect(reverse('person-details', args=(person_id,)))
    else:
        if phone_id:
            phone = get_object_or_404(Phone, id=phone_id)
            additional_data = PhoneService.build_additional_data(phone)
            initial_data.update(additional_data)

        form = PhoneForm(initial=initial_data)

    return render_to_response("phone/edit.html", {'form': form}, context_instance=RequestContext(request))


@permission_required('auth.management_metropol')
def delete(request, phone_id):
    phone = get_object_or_404(Phone, id=phone_id)
    person_id = phone.person.id
    phone.delete()
    messages.success(request, "Se ha borrado el teléfono correctamente.")

    return HttpResponseRedirect(reverse('person-details', args=(person_id,)))
