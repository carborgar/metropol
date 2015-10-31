from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.views import generic
from django.db.models import Q

from metropol_abogados.services import ExpedientService
from metropol_abogados.models import Expedient
from metropol_abogados.forms import ExpedientForm, ExpedientListFilterForm


def get_redirect(request, expedient_id):
    msg = "Expediente %s correctamente" % ("guardado" if not expedient_id else "editado")
    messages.success(request, msg)
    if expedient_id:
        return HttpResponseRedirect(reverse('expedient-details', args=(expedient_id,)))
    else:
        return HttpResponseRedirect(reverse('expedient-list'))


@permission_required('auth.management_metropol')
def edit(request, expedient_id=None):
    if request.method == 'POST':
        form = ExpedientForm(request.POST)
        if form.is_valid():
            ExpedientService.save_from_form(form)

            return get_redirect(request, expedient_id)
    else:
        initial_data = {'expedient_num': Expedient.objects.latest().id + 1}

        if expedient_id:
            expedient = get_object_or_404(Expedient, id=expedient_id)
            initial_data = ExpedientService.build_initial_data(expedient)

        form = ExpedientForm(initial=initial_data)

    return render_to_response("expedient/edit.html", {'form': form}, context_instance=RequestContext(request))


@permission_required('auth.management_metropol')
def expedient_list(request):
    form = ExpedientListFilterForm(request.GET)
    expedients = ExpedientService.find_all()

    if form.is_valid():
        search_term = form.cleaned_data['keyword'] or None
        selected_branch_id = form.cleaned_data['branch'] or None
        selected_headquarters_id = form.cleaned_data['headquarters'] or None
        selected_state = form.cleaned_data['state'] or None
        selected_customers = form.cleaned_data['customers'] or None

        if search_term:
            expedients = expedients.filter(Q(id__icontains=search_term) | Q(description__icontains=search_term))

        # Remember -> -1 equals "without" and None is "all"
        if selected_branch_id:
            if selected_branch_id == '-1':
                # Filter expedients without branch
                expedients = expedients.filter(phase__isnull=True)
            else:
                expedients = expedients.filter(phase__law_branch__id=selected_branch_id)

        if selected_headquarters_id:
            if selected_headquarters_id == '-1':
                # Filter expedients without headquarters
                expedients = expedients.filter(headquarters__isnull=True)
            else:
                expedients = expedients.filter(headquarters__id=selected_headquarters_id)

        if selected_state:
            expedients = expedients.filter(state=selected_state)

        if selected_customers:
            expedients = expedients.filter(expperrol__person__in=selected_customers, expperrol__role__text_help__iexact='CLIENTE').distinct()

    return render_to_response("expedient/list.html", {"expedients": expedients, 'filter_form': form}, context_instance=RequestContext(request))


class DetailsView(generic.DetailView):
    model = Expedient
    template_name = 'expedient/details.html'


@permission_required('auth.management_metropol')
def delete(request, expedient_id):
    expedient = get_object_or_404(Expedient, id=expedient_id)
    expedient.delete()
    messages.success(request, "Se ha borrado el expediente correctamente.")

    return HttpResponseRedirect(reverse('expedient-list'))
