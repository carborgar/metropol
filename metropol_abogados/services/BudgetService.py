from metropol_abogados.models import Budget


def save_from_form(budget_form, expedient):
    budget_form.cleaned_data.update({'expedient': expedient})

    return Budget.objects.update_or_create(id=expedient.budget.id if expedient.has_budget() else None,
                                           defaults=budget_form.cleaned_data)


def build_additional_data(budget):
    return {'state_budget': budget.state_budget, 'amount': budget.amount, 'own_attorney': budget.own_attorney,
            'description': budget.description}
