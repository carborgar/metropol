from django.shortcuts import render_to_response
from django.template import RequestContext
from metropol_abogados.services import PersonService
from metropol_abogados.models import Person, Role
from metropol_abogados.forms import PersonListFilterForm, PersonForm
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.views import generic


def get_redirect(request, person_id):
    msg = "Persona %s correctamente" % ("guardada" if not person_id else "editada")
    messages.success(request, msg)
    if person_id:
        return HttpResponseRedirect(reverse('person-details', args=(person_id,)))
    else:
        return HttpResponseRedirect(reverse('person-list'))


@permission_required('auth.management_metropol')
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


@permission_required('auth.management_metropol')
def person_list(request):
    form = PersonListFilterForm(request.GET)
    order_by = request.GET.get('order_by', 'name')
    persons = Person.objects.order_by(order_by)

    selected_role_id = request.GET.get('role') or None
    search_term = request.GET.get('keyword') or None

    if search_term:
        persons = persons.filter(Q(name__icontains=search_term) | Q(id_number__icontains=search_term) | Q(email__icontains=search_term))

    if form.is_valid() and selected_role_id:
        # The user selected a role. Role -1 means "without role" (for old database compatibility)
        if selected_role_id == '-1':
            # Search persons without a role
            persons = persons.filter(expperrol__isnull=True)
        else:
            selected_role = get_object_or_404(Role, id=selected_role_id)
            persons = persons.filter(expperrol__role__in=[selected_role]).distinct()

    return render_to_response("person/list.html", {"persons": persons, 'filter_form': form},
                              context_instance=RequestContext(request))


class DetailsView(generic.DetailView):
    model = Person
    template_name = 'person/details.html'


@permission_required('auth.management_metropol')
def delete(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    assert not person.expperrol_set.all(), "No se puede borrar esta persona porque tiene expedientes asociados."
    person.delete()
    messages.success(request, "Se ha borrado la persona correctamente.")

    return HttpResponseRedirect(reverse('person-list'))
