# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required

from metropol_abogados.services import PaymentService
from metropol_abogados.models import Payment, Budget
from metropol_abogados.forms import PaymentForm


@permission_required('auth.management_metropol')
def edit(request, payment_id=None, budget_id=None):

    payment = get_object_or_404(Payment, id=payment_id) if payment_id else None

    # One of "payment_id" or "budget_id" will be present
    if budget_id:
        # Creating a new payment
        budget = get_object_or_404(Budget, id=budget_id)
    else:
        # Editing an existing payment
        budget = payment.budget

    initial_data = {'budget': budget}
    expedient = budget.expedient

    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():
            obj, created = PaymentService.save_from_form(form, budget, payment)

            messages.success(request, "Pago %s correctamente" % ("guardado" if created else "editado"))

            return HttpResponseRedirect('{}#budget-payment'.format(reverse('expedient-details', args=(expedient.id,))))

    else:
        if payment:
            additional_data = PaymentService.build_additional_data(payment)
            initial_data.update(additional_data)

        form = PaymentForm(initial=initial_data)

    return render_to_response("payment/edit.html", {'form': form, 'expedient': expedient, 'creating': not payment}, context_instance=RequestContext(request))


@permission_required('auth.management_metropol')
def delete(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    expedient_id = payment.budget.expedient.id

    payment.delete()
    messages.success(request, "Se ha borrado el pago correctamente.")

    return HttpResponseRedirect('{}#budget-payment'.format(reverse('expedient-details', args=(expedient_id,))))
