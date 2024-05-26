import logging
from django.shortcuts import render

from treeflow.corpus.forms.line_form import CreateLineSectionForm, AssignLineSectionForm
from treeflow.corpus.models.token import Token


logger = logging.getLogger(__name__)

from django.template.loader import render_to_string

def line_form_view(request, token_id):
    token = Token.objects.get(pk=token_id)
    create_form = CreateLineSectionForm()  # Initialize forms at the beginning
    assign_form = AssignLineSectionForm()

    if request.method == 'POST':
        if 'create_line' in request.POST:
            create_form = CreateLineSectionForm(request.POST)  # Reassign if POST
            if create_form.is_valid():
                new_line = create_form.save(commit=False)
                new_line.type = 'line'  # Ensure the type is set to 'line'
                new_line.save()
                create_form = CreateLineSectionForm()  # Reinitialize the form
                assign_form = AssignLineSectionForm()  # Ensure other form is also reset
                return render(request, 'line_modal.html', {
                    'token': token,
                    'create_form': create_form,
                    'assign_form': assign_form
                })
            
        elif 'assign_line' in request.POST:
            assign_form = AssignLineSectionForm(request.POST)  # Reassign if POST
            if assign_form.is_valid():
                token.line_section = assign_form.cleaned_data['line_section']
                token.save()
                # pass the data to line_data and then to line_update
                line_data = render_to_string('line_data.html', {'token': token})
                return render(request, 'line_update.html', {'line_data': line_data, 'token_id': token_id})
            
    if request.method == 'GET':
        token = Token.objects.get(pk=token_id)
        create_form = CreateLineSectionForm()  # Initialize forms at the beginning
        assign_form = AssignLineSectionForm()

        return render(request, 'line_modal.html', {
            'token': token,
            'create_form': create_form,
            'assign_form': assign_form
        })

