from treeflow.corpus.forms.section_form import SectionForm
from django.shortcuts import render

def load_section_modal(request):
    selected_tokens = request.GET.get('tokens', '')
    form = SectionForm(initial={'selected_tokens': selected_tokens})
    return render(request, 'section_modal.html', {'form': form})