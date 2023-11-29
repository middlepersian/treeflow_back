from django.shortcuts import render
from django.core.paginator import Paginator
from treeflow.corpus.models import Text, Section


def sections_view(request):
    # Get all Text and Section types for the dropdowns
    texts = Text.objects.all()
    section_types = Section.objects.order_by('type').values_list('type', flat=True).distinct()

    # Retrieve GET parameters
    selected_text_id = request.GET.get('text_id')
    selected_section_type = request.GET.get('section_type')

    # Start with an initial sections queryset
    # and prefetch related data to minimize database hits
    sections = Section.objects.prefetch_related(
        'sectiontoken_set__token__lemmas',  # Prefetch lemmas through TokenLemma
        'sectiontoken_set__token__senses',  # Prefetch meanings through TokenSense
        'sectiontoken_set__token__pos_token'  # Prefetch related POS objects
    ).order_by('number')

    # Filter sections if a text ID is provided
    if selected_text_id:
        sections = sections.filter(text__id=selected_text_id)

    # Filter sections if a section type is provided
    if selected_section_type:
        sections = sections.filter(type=selected_section_type)

    # Setup paginator
    paginator = Paginator(sections, 10)  # Show 10 sections per page
    page_number = request.GET.get('page')
    sections_page = paginator.get_page(page_number)

    # Prepare context for rendering
    context = {
        'texts': texts,
        'section_types': section_types,
        'sections': sections,
        'selected_text_id': selected_text_id or '',
        'selected_section_type': selected_section_type,
    }

    # Render response
    return render(request, 'sections.html', context)