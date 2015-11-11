# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required

from metropol_abogados.services import BudgetService
from metropol_abogados.models import Expedient
from metropol_abogados.forms import BudgetForm


@permission_required('auth.management_metropol')
def edit(request, expedient_id):
    expedient = get_object_or_404(Expedient, id=expedient_id)
    initial_data = {'expedient': expedient}

    if request.method == 'POST':
        form = BudgetForm(request.POST)

        if form.is_valid():
            obj, created = BudgetService.save_from_form(form, expedient)

            messages.success(request, "Presupuesto %s correctamente" % ("guardado" if created else "editado"))

        return HttpResponseRedirect('{}#budget-payment'.format(reverse('expedient-details', args=(expedient.id,))))

    else:
        if expedient.has_budget:
            budget = expedient.budget
            additional_data = BudgetService.build_additional_data(budget)
            initial_data.update(additional_data)

        form = BudgetForm(initial=initial_data)

    return render_to_response("budget/edit.html", {'form': form, 'expedient': expedient},
                              context_instance=RequestContext(request))


@permission_required('auth.management_metropol')
def delete(request, expedient_id):
    get_object_or_404(Expedient, id=expedient_id).budget.delete()

    messages.success(request, "Se ha borrado el presupuesto correctamente.")

    return HttpResponseRedirect('{}#budget-payment'.format(reverse('expedient-details', args=(expedient_id,))))
