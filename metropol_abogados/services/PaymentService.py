from metropol_abogados.models import Payment


def save_from_form(payment_form, budget, payment):
    payment_form.cleaned_data.update({'budget': budget})

    return Payment.objects.update_or_create(id=payment.id if payment else None, defaults=payment_form.cleaned_data)


def build_additional_data(payment):
    return {'amount': payment.amount, 'date': payment.date}
