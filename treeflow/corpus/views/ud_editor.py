from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from treeflow.corpus.models import (
    Token,
    Dependency,
    Section,
    SectionToken,
)  # Adjust to your model's import path
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q


def calculate_positions(word_length_1, x1, font_size, gap):
    char_width = font_size * 0.6
    word_width_1 = word_length_1 * char_width

    x2 = x1 + word_width_1 + gap

    return x1, x2


def ud_editor(request, section_id):
    # Get the section
    section = get_object_or_404(Section, pk=section_id, type="sentence")

    if request.method == "POST" and request.POST.get("dependency"):
        from_token_id = request.POST.get("from")
        to_token_id = request.POST.get("to")
        from_token = Token.objects.get(from_token_id)
        to_token = Token.objects.get(to_token_id)

        dep = Dependency.objects.create(token=from_token_id, head=to_token_id)
        dep.save()
        return HTTPRedirectResponse(".")
    
    section_tokens = section.tokens.all()
    tokens = list(section_tokens)

    dependencies = (
        Dependency.objects.filter(Q(token__in=tokens) | Q(head__in=tokens))
        .select_related("token", "head")
        .distinct()
    )

    token_data = []
    x1 = 0
    for token in tokens:
        token_dependencies = []
        x1, x2 = calculate_positions(len(token.transcription), x1, 12, 10)

        for dep in dependencies:
            if dep.token == token:
                token_dependencies.append(
                    {
                        "id": dep.id,
                        "from_token_id": {
                            "id": dep.token.id,
                            "transcription": dep.token.transcription,
                            "xpos": x1 if dep.token.number_in_sentence else 0,
                            "ypos": 50 if dep.token.number_in_sentence else 0,
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
                "xpos": x1 if token.number_in_sentence else 0,
                "ypos": 50 if token.number_in_sentence else 0,
                "transcription": token.transcription,
                "dep_len": len(token_dependencies),
                "dependencies": token_dependencies,
            }
        )
        x1 = x2

    # Prepare context for the template
    context = {
        "section": section,
        "tokens": token_data,
    }

    # Render the template
    return render(request, "ud_editor.html", context)
