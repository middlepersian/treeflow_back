from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from treeflow.corpus.models import Token, Dependency, Section, SectionToken  # Adjust to your model's import path
from django.db.models import Q

def ud_editor(request, section_id):
    # Get the section by ID and ensure it's of type 'sentence'
    section = get_object_or_404(Section, pk=section_id, type='sentence')

    # Get all SectionToken instances for the section
    section_tokens = section.tokens.all()

    # Extract token instances from section_tokens
    tokens = [t for t in section_tokens]

    # Now get all dependencies for those tokens
    dependencies = Dependency.objects.filter(
        Q(token__in=tokens) | Q(head__in=tokens)
    ).select_related('token', 'head').distinct()

    # Prepare token and dependency data
    token_data = [{'id': token.id, 'transcription': token.transcription} for token in tokens]
    dependency_data = [{
        'id': dep.id,
        'from_token_id': dep.token.id,
        'to_token_id': dep.head.id if dep.head else None,
        'rel': dep.rel,
        'enhanced': dep.enhanced
    } for dep in dependencies]

    # Prepare context for the template
    context = {
        'section': section,
        'tokens': token_data,
        'dependencies': dependency_data,
    }

    # Render the template
    return render(request, 'ud_editor.html', context)