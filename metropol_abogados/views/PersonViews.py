__author__ = 'Carlos'

from metropol_abogados.forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from metropol_abogados.services import PersonService
from metropol_abogados.models import Person, Role
from metropol_abogados.forms import PersonListFilterForm
from django.shortcuts import get_object_or_404


def edit(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            PersonService.save_from_form(form)
    else:
        form = PersonForm()

    return render_to_response("person/edit.html", {'form': form}, context_instance=RequestContext(request))


def person_list(request):
    form = PersonListFilterForm(request.GET)
    order_by = request.GET.get('order_by', 'name')
    persons = Person.objects.order_by(order_by)

    selected_role = request.GET.get('role') or None
    search_term = request.GET.get('keyword') or None

    if search_term:
        persons = persons.filter(name__icontains=search_term)

    if form.is_valid() and selected_role:
        persons = persons.filter(expperrol__role__in=[selected_role]).distinct()

    return render_to_response("person/list.html", {"persons": persons, 'filter_form': form},
                              context_instance=RequestContext(request))


def details(request, person_id):
    person = get_object_or_404(Person, id=person_id)

    return render_to_response("person/details.html", {"person": person}, context_instance=RequestContext(request))
