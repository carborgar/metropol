__author__ = 'Carlos'

from django.shortcuts import render_to_response
from django.template import RequestContext
from metropol_abogados.services import PersonService
from metropol_abogados.models import Person
from metropol_abogados.forms import PersonListFilterForm, PersonForm
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
import datetime


def get_redirect(request, person_id):
    msg = "Persona %s correctamente" % ("guardada" if not person_id else "editada")
    messages.success(request, msg)
    if person_id:
        return HttpResponseRedirect(reverse('person-details', args=(person_id,)))
    else:
        return HttpResponseRedirect(reverse('person-list'))


def edit(request, person_id=None):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            PersonService.save_from_form(form)

            return get_redirect(request, person_id)
    else:
        initial_data = {}

        if person_id:
            person = get_object_or_404(Person, id=person_id)
            initial_data = PersonService.build_initial_data(person)

        form = PersonForm(initial=initial_data)

    return render_to_response("person/edit.html", {'form': form}, context_instance=RequestContext(request))


def person_list(request):
    form = PersonListFilterForm(request.GET)
    order_by = request.GET.get('order_by', 'name')
    persons = Person.objects.order_by(order_by)

    selected_role = request.GET.get('role') or None
    search_term = request.GET.get('keyword') or None

    if search_term:
        persons = persons.filter(Q(name__icontains=search_term) | Q(id_number__icontains=search_term) | Q(email__icontains=search_term))

    if form.is_valid() and selected_role:
        persons = persons.filter(expperrol__role__in=[selected_role]).distinct()

    return render_to_response("person/list.html", {"persons": persons, 'filter_form': form},
                              context_instance=RequestContext(request))


def details(request, person_id):
    person = get_object_or_404(Person, id=person_id)

    return render_to_response("person/details.html", {"person": person}, context_instance=RequestContext(request))


def delete(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    assert not person.expperrol_set.all(), "No se puede borrar esta persona porque tiene expedientes asociados."
    person.delete()
    messages.success(request, "Se ha borrado la persona correctamente.")

    return HttpResponseRedirect(reverse('person-list'))
