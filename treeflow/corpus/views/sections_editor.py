from django.shortcuts import render
from django.db.models import Prefetch
from treeflow.corpus.models import Section, Token
from django.db.models import Count, Prefetch


from collections import defaultdict

def build_tree(sections):
    tree = defaultdict(list)
    sections_dict = {section.id: section for section in sections}

    # Organize sections by their container
    for section in sections:
        parent_id = section.container_id if section.container else None
        tree[parent_id].append(section)

    # Sort sections within the same container
    for parent_id, children in tree.items():
        sorted_children = sorted(
            children, 
            key=lambda x: (x.previous is not None, getattr(x.previous, 'id', None))
        )
        tree[parent_id] = sorted_children

    return dict(tree)


def sections_editor_view(request, text_id):
    # Define the queryset for tokens that prefetches the related section tokens for 'sentence' type sections
    token_queryset = Token.objects.filter(
        sectiontoken__section__text_id=text_id,
        sectiontoken__section__type='sentence'
    ).order_by('sectiontoken__section__number', 'number_in_sentence')

    # Create a Prefetch object for 'tokens' related to 'sentence' type sections
    tokens_prefetch = Prefetch(
        'tokens', 
        queryset=token_queryset,
        to_attr='prefetched_tokens'
    )

    # Fetch all sections for the given text, applying the Prefetch object conditionally
    all_sections = Section.objects.filter(text__id=text_id)
    sentence_sections = all_sections.filter(type='sentence').prefetch_related(tokens_prefetch)
    other_sections = all_sections.exclude(type='sentence')

    # Build a tree of sections
    section_tree = build_tree(all_sections)    

    # Get distinct section types
    section_types = Section.objects.order_by('type').values_list('type', flat=True).distinct()
    # Pass the sentence_sections with prefetched tokens and other sections to the template
    context = {
        'sentence_sections': sentence_sections,
        'other_sections': other_sections,
        'section_types': section_types,
        'section_tree': section_tree,
    }

    return render(request, 'sections_editor.html', context)
