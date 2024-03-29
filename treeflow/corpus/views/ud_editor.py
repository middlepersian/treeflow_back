from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from ..enums.deprel_enum import Deprel
from treeflow.corpus.models import (
    Token,
    Dependency,
    Section,
    SectionToken,
    Feature,
    POS
)  # Adjust to your model's import path
from treeflow.dict.models import Sense, Lemma
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q


# Adjust this function to account for a dynamic gap between tokens
def calculate_positions(word_length_1, x1, font_size, gap, additional_space):
    char_width = font_size * 0.6
    word_width_1 = word_length_1 * char_width

    # Add the additional space to the gap
    x2 = x1 + word_width_1 + gap + additional_space

    return int(x1), int(x2)



def deleteDependency(request):
    if request.method == "POST":
        dep_id = request.POST.get("dep_id")
        dep = Dependency.objects.get(id=dep_id)
        
        # also check if other dependencies for that token have the Root relation
        # if not, set the token.root to True
        if dep.rel == Deprel.ROOT:
            token = dep.token
            other_deps = Dependency.objects.filter(token=token).exclude(id=dep_id)
            if not other_deps.filter(rel=Deprel.ROOT).exists():
                token.root = False
                token.save()
        dep.delete()

        return HttpResponseRedirect("/corpus/ud-editor/" + str(request.POST.get("section_id")) + "/")
    else:
        return HttpResponse("Error")

def setNewRoot(request):
    if request.method == "POST":
        token_id = request.POST.get("token_id")
        token = Token.objects.get(id=token_id)
        newDep = Dependency.objects.create(token=token, rel=Deprel.ROOT)
        newDep.save()
        token.root = True
        token.save()
        return HttpResponseRedirect("/corpus/ud-editor/" + str(request.POST.get("section_id")) + "/")
    else:
        return HttpResponse("Error")    

def saveNewDependency(request):
    if request.method == "POST":
        from_token_id = request.POST.get("from")
        to_token_id = request.POST.get("to")
        dep_type = request.POST.get("depType")
        enhanced = bool(request.POST.get("enhanced"))
        from_token = Token.objects.get(id=from_token_id)
        to_token = Token.objects.get(id=to_token_id)

        dep = Dependency.objects.create(token=from_token, head=to_token,rel=Deprel[dep_type], enhanced=enhanced)
        dep.save()
        return HttpResponseRedirect("/corpus/ud-editor/" + str(request.POST.get("section_id")) + "/")
    else:
        return HttpResponse("Error")
    
    

def ud_editor(request, section_id):
    # Get the section
    section = get_object_or_404(Section, pk=section_id, type="sentence")
    prev, next = section.find_adjacent_sections(section_id)
    section_tokens = section.tokens.all()
    tokens = list(section_tokens)
    senses = Sense.objects.filter(token_senses__in=tokens).select_related("token_senses").distinct()
    dependencies = (
        Dependency.objects.filter(Q(token__in=tokens) | Q(head__in=tokens))
        .select_related("token", "head")
        .distinct()
    )
    posList = (
        POS.objects.filter(Q(token__in=tokens)).select_related("token").distinct()
    )
    featureList = (Feature.objects.filter(Q(token__in=tokens)).select_related("token").distinct())
    token_data = []
    additional_space = 30
    x1 = 0

    for token in tokens:
        token_dependencies = []
        token_pos = []
        # Check if transcription is None or an empty string before calling len()
        transcription_length = 0 if token.transcription is None else len(token.transcription)
        x1, x2 = calculate_positions(transcription_length, x1, 12, 10, additional_space)
        for pos in posList:
            if pos.token == token:
                token_pos.append(
                    {
                    "id":pos.id,
                     "pos":pos.pos,
                     "type":pos.type,
                     "features": [
                         {"name":feature.feature, "value":feature.feature_value} for feature in featureList if feature.token == token and feature.pos == pos
                     ]
                     }
                )



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
                "root": token.root,
                "xpos": x1 if token.number_in_sentence else 0,
                "ypos": 50 if token.number_in_sentence else 0,
                "transcription": token.transcription,
                "lemma": [lemma.word for lemma in token.lemmas.all()],
                "transliteration": token.transliteration,
                "senses": [sense.sense for sense in token.senses.all()],
                "pos_len": len(token_pos),
                "pos": token_pos,
                "dep_len": len(token_dependencies),
                "dependencies": token_dependencies,            
            }
        )
        x1 = x2

    # Prepare context for the template
    context = {
        "section": section,
        "prev" : prev,
        "next" : next,
        "tokens": token_data,
        "deprel": {d.name: d for d in Deprel},
    }

    # Render the template
    return render(request, "ud_editor.html", context)
