from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from treeflow.corpus.models import (
    Token,
    Dependency,
    Section,
    SectionToken,
)  # Adjust to your model's import path
from django.db.models import Q


def ud_editor(request, section_id):
    # Get the section by ID and ensure it's of type 'sentence'
    section = get_object_or_404(Section, pk=section_id, type="sentence")

    # Get all SectionToken instances for the section
    section_tokens = section.tokens.all()

    # Extract token instances from section_tokens
    tokens = list(section_tokens)

    # Now get all dependencies for those tokens
    dependencies = (
        Dependency.objects.filter(Q(token__in=tokens) | Q(head__in=tokens))
        .select_related("token", "head")
        .distinct()
    )

    # Prepare token and dependency data
    token_data = []
    for token in tokens:
        token_dependencies = []
        for dep in dependencies:
            if dep.token == token:
                token_dependencies.append(
                    {
                        "id": dep.id,
                        "from_token_id": {
                            "id": dep.token.id,
                            "transcription": dep.token.transcription,
                            "xpos": dep.token.number_in_sentence * 50
                            if dep.token.number_in_sentence
                            else 0,
                            "ypos": dep.token.number_in_sentence * 50
                            if dep.token.number_in_sentence
                            else 0,
                        },
                        "to_token_id": {
                            "id": dep.head.id,
                            "transcription": dep.head.transcription,
                        }
                        if dep.head
                        else None,
                        "rel": dep.rel,
                        "enhanced": dep.enhanced,
                    }
                )
        token_data.append(
            {
                "id": token.id,
                "number": token.number_in_sentence,
                "xpos": token.number_in_sentence * 50
                if token.number_in_sentence
                else 0,
                "ypos": token.number_in_sentence * 50
                if token.number_in_sentence
                else 0,
                "transcription": token.transcription,
                "dep_len": len(token_dependencies),
                "dependencies": token_dependencies,
            }
        )

    # Prepare context for the template
    context = {
        "section": section,
        "tokens": token_data,
    }

    # Render the template
    return render(request, "ud_editor.html", context)
