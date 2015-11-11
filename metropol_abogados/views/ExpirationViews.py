# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.views.generic.detail import DetailView

from metropol_abogados.services import ExpirationService
from metropol_abogados.models import Expiration, Expedient
from metropol_abogados.forms import ExpirationForm


class DetailsView(DetailView):
    model = Expiration
    template_name = 'expiration/details.html'


@permission_required('auth.management_metropol')
def edit(request, expedient_id=None, expiration_id=None):
    # One of "expedient_id" or "expiration_id" will be present
    if expedient_id:
        expedient = get_object_or_404(Expedient, id=expedient_id)
    else:
        expedient = get_object_or_404(Expiration, id=expiration_id).expedient

    initial_data = {'expedient': expedient}
    available_events = expedient.available_events()

    if request.method == 'POST':
        form = ExpirationForm(request.POST, available_events=available_events)

        if form.is_valid():
            obj, created = ExpirationService.save_from_form(form)

            messages.success(request, "Vencimiento %s correctamente" % ("guardado" if created else "editado"))

        return HttpResponseRedirect('{}#expiration'.format(reverse('expedient-details', args=(expedient.id,))))

    else:
        if expiration_id:
            expiration = get_object_or_404(Expiration, id=expiration_id)
            additional_data = ExpirationService.build_additional_data(expiration)
            initial_data.update(additional_data)

        form = ExpirationForm(initial=initial_data, available_events=available_events)

    return render_to_response("expiration/edit.html", {'form': form, 'expedient': expedient},
                              context_instance=RequestContext(request))


@permission_required('auth.management_metropol')
def delete(request, expiration_id):
    expiration = get_object_or_404(Expiration, id=expiration_id)
    expedient_id = expiration.expedient.id
    expiration.delete()
    messages.success(request, "Se ha borrado el vencimimento correctamente.")

    return HttpResponseRedirect('{}#expiration'.format(reverse('expedient-details', args=(expedient_id,))))
