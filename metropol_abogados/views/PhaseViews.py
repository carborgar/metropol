from metropol_abogados.models import LawBranch
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse


@permission_required('auth.management_metropol')
def phase_by_branch_json(request):
    branch = get_object_or_404(LawBranch, id=request.GET['branch'])
    json_content = [{'label': phase.name, 'value': phase.id} for phase in branch.phase_set.all()]

    return JsonResponse(json_content, safe=False)
