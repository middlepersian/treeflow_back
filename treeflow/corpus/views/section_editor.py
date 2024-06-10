from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from treeflow.corpus.models import Section
from treeflow.corpus.forms.section_editor_form import SectionEditorForm
from treeflow.dict.forms.sense_form import SenseForm  # Import the SenseForm
import logging

from huey.contrib.djhuey import db_task


logger = logging.getLogger(__name__)

def section_editor_form_view(request, section_id=None):
    logger.debug("section_editor_form_view")
    logger.debug("section_id: %s" % section_id)

    if section_id:
        section = get_object_or_404(Section, id=section_id)
        form = SectionEditorForm(request.POST or None, instance=section)
    else:
        form = SectionEditorForm(request.POST or None)

    sense_form = SenseForm()  # Create an instance of SenseForm

    return render(request, 'section_editor_form.html', {'form': form, 'sense_form': sense_form, 'section_id': section_id})


def section_merge(request,section_id=None):
    """ 
        Merge two sections of type "sentence"
        Post Request, requires section_id, only for authenticated users
        
    """
    logger.debug("section_merge %s" % section_id)
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'User not authenticated'})
    
    section_source = get_object_or_404(Section,id=section_id)
    if section_source.type != "sentence":
        return JsonResponse({'status': 'error', 'message': 'Section is not of type sentence'})
    if not section_source.next:
        return JsonResponse({'status': 'error', 'message': 'Section has no next section'})

    section_target = section_source.next
    if section_target.type != "sentence":
        return JsonResponse({'status': 'error', 'message': 'Next section is not of type sentence'})
    
    logger.debug("source: %s" % section_source, "target: %s" % section_target)

    # targets next is now sources next
    new_next = section_target.next
    section_source.next = new_next

    # get highest token number in source        
    last_token_source_number = 0.0
    last_token_source = section_source.tokens.last()
    if last_token_source:
        last_token_source_number = last_token_source.number_in_sentence
    
    # add all tokens from target to source and renumber them
    for token in section_target.tokens.all():
        section_source.tokens.add(token)
        section_target.tokens.remove(token)
        last_token_source_number += 1.0
        token.number_in_sentence = last_token_source_number
        token.save()
    
    # save changes
    section_source.save()
    section_target.save()

    return JsonResponse({'status': 'success', 'message': 'Sections merged successfully'})


def renumber_sections(request):
    """
        Renumbers all sections in a text based on their order, to close gaps in numbering, only for authenticated users
    """
    logger.debug("renumber_sections")
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'User not authenticated'})
    try:
        text_id = request.POST.get('text_id')
    except:
        return JsonResponse({'status': 'error', 'message': 'Text ID not provided'})
    
    _renumber_sections(text_id)
    return JsonResponse({'status': 'success', 'message': 'Sections renumbered successfully'})

@db_task()
def _renumber_sections(text_id):
    sections = Section.objects.filter(text_id=text_id, type="sentence").order_by('order')
    logger.debug("sections: %s" % sections)
    i = 1.0
    for section in sections:
        section.number = i
        section.save()
        i += 1.0