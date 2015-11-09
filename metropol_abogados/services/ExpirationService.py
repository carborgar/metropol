from metropol_abogados.models import Expiration


def save_from_form(expiration_form):
    new_data = expiration_form.cleaned_data
    expiration = new_data['expiration']

    del new_data['expiration']

    return Expiration.objects.update_or_create(id=expiration.id if expiration else None, defaults=new_data)


def build_additional_data(expiration):
    return {'expiration': expiration, 'expedient': expiration.expedient, 'date': expiration.date,
            'place': expiration.place, 'description': expiration.description, 'event': expiration.event}
