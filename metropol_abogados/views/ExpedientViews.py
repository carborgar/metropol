from django.shortcuts import render_to_response
from django.template import RequestContext
from metropol_abogados.services import ExpedientService
from metropol_abogados.models import  Expedient
from metropol_abogados.forms import  ExpedientForm
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.views import generic


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
        initial_data = {}

        if expedient_id:
            expedient = get_object_or_404(Expedient, id=expedient_id)
            initial_data = ExpedientService.build_initial_data(expedient)

        form = ExpedientForm(initial=initial_data)

    return render_to_response("expedient/edit.html", {'form': form}, context_instance=RequestContext(request))


@permission_required('auth.management_metropol')
def expedient_list(request):
    eps = ExpedientService.find_all()

    return render_to_response("expedient/list.html", {"expedients": eps}, context_instance=RequestContext(request))


@permission_required('auth.management_metropol')
class DetailsView(generic.DetailView):
    model = Expedient
    template_name = 'expedient/details.html'


@permission_required('auth.management_metropol')
def delete(request, expedient_id):
    expedient = get_object_or_404(Expedient, id=expedient_id)
    expedient.delete()
    messages.success(request, "Se ha borrado el expediente correctamente.")

    return HttpResponseRedirect(reverse('expedient-list'))
