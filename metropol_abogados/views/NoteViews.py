# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required

from metropol_abogados.models import Address, Note
from metropol_abogados.forms import NoteForm


@permission_required('auth.management_metropol')
def edit(request):
    note_form = NoteForm(request.POST)

    # Don't validate when deleting

    note_form.is_valid()

    form_note = note_form.cleaned_data.get('note')
    form_person = note_form.cleaned_data.get('person')
    form_expedient = note_form.cleaned_data.get('expedient')
    form_description = note_form.cleaned_data.get('description')

    redir_id, view_name = (form_person.id, 'person-details') if form_person else (form_expedient.id, 'expedient-details')

    # Initialize the result message
    message_action_key = None

    if request.POST.get('delete'):
            form_note.delete()
            message_action_key = 'borrada'

    elif note_form.is_valid():
        new_data = {'person': form_person, 'expedient': form_expedient, 'description': form_description}
        obj, created = Note.objects.update_or_create(id=form_note.id if form_note else None, defaults=new_data)

        message_action_key = 'creada' if created else 'editada'

    else:
        messages.error(request, "Ha ocurrido un error.")

    # Save edition/creation message if needed
    if message_action_key:
        messages.success(request, "Nota %s correctamente" % message_action_key)

    return HttpResponseRedirect(reverse(view_name, args=(redir_id,)))


@permission_required('auth.management_metropol')
def delete(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    person_id = address.person.id
    address.delete()
    messages.success(request, "Se ha borrado la dirección correctamente.")

    return HttpResponseRedirect(reverse('person-details', args=(person_id,)))
