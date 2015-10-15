from metropol_abogados.models import Expedient, ExpPerRol, Role, Phase
from metropol_abogados.utils import DateUtils


def save_from_form(expedient_form):
    expedient = Expedient()
    # If id is present, get the DB person and edit
    expedient_id = expedient_form.cleaned_data['id']

    if expedient_id:
        expedient = Expedient.objects.get(id=expedient_id)

    expedient.id = expedient_form.cleaned_data['expedient_num']
    expedient.description = expedient_form.cleaned_data['description']
    form_creation_date = expedient_form.cleaned_data['creation_date']
    form_end_date = expedient_form.cleaned_data['end_date'] or None
    expedient.creation_date = DateUtils.convert_date_to_datetime(form_creation_date)
    expedient.end_date = DateUtils.convert_date_to_datetime(form_end_date)
    expedient.user_type = expedient_form.cleaned_data['user_type']
    expedient.phase = Phase.objects.get(id=expedient_form.cleaned_data['phase'])
    expedient.state = expedient_form.cleaned_data['state']
    expedient.headquarters = expedient_form.cleaned_data['headquarters']

    expedient.save()

    # Save ExpPerRol entities
    save_exps(expedient_form, expedient)


def save_exps(expedient_form, expedient):
    expedient_id = expedient_form.cleaned_data['id']

    customer_role = Role.objects.get(text_help__iexact="CLIENTE")
    contrary_role = Role.objects.get(text_help__iexact="CONTRARIO")
    contrary_lawyer_role = Role.objects.get(text_help__iexact="ABOGADO_CONTRARIO")
    attorney_role = Role.objects.get(text_help__iexact="PROCURADOR")

    customers = expedient_form.cleaned_data['customers']
    contraries = expedient_form.cleaned_data['contraries']
    contrary_lawyers = expedient_form.cleaned_data['contrary_lawyers']
    attorneys = expedient_form.cleaned_data['attorneys']

    if expedient_id:
        # TODO think on a more efficient solution
        # Delete existing expperrol_set
        database_expedient = Expedient.objects.get(id=expedient_id)
        database_expedient.expperrol_set.all().delete()

    # Create all (bulk mode for efficient insert)
    ExpPerRol.objects.bulk_create(
        [ExpPerRol(person=customer, expedient=expedient, role=customer_role) for customer in customers] +
        [ExpPerRol(person=contrary, expedient=expedient, role=contrary_role) for contrary in contraries] +
        [ExpPerRol(person=cl, expedient=expedient, role=contrary_lawyer_role) for cl in contrary_lawyers] +
        [ExpPerRol(person=attorney, expedient=expedient, role=attorney_role) for attorney in attorneys]
    )


def find_all():
    return Expedient.objects.all()


def build_initial_data(expedient):
    return {'id': expedient.id, 'expedient_num': expedient.id, 'branch': expedient.phase.law_branch,
            'phase': expedient.phase,
            'state': expedient.state, 'headquarters': expedient.headquarters, 'user_type': expedient.user_type,
            'description': expedient.description, 'customers': expedient.customers(),
            'contraries': expedient.contraries(),
            'contrary_lawyers': expedient.contrary_lawyers(), 'attorneys': expedient.attorneys(),
            'creation_date': expedient.creation_date, 'end_date': expedient.end_date}
