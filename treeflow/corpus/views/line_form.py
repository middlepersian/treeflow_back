import logging
from django.shortcuts import render
from treeflow.corpus.forms.line_form import CreateLineSectionForm, AssignLineSectionForm
from treeflow.corpus.models.token import Token
from treeflow.corpus.models.section import Section
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def line_form_view(request, token_id):
    token = Token.objects.get(pk=token_id)

    if request.method == "POST":
        if "create_line" in request.POST:
            create_form = CreateLineSectionForm(request.POST)  # Reassign if POST
            if create_form.is_valid():
                new_line = create_form.save(commit=False)
                new_line.type = "line"  # Ensure the type is set to 'line'
                new_line.text = token.text
                new_line.save()
                create_form = CreateLineSectionForm()  # Reinitialize the form
                assign_form = AssignLineSectionForm(text_id=token.text.id)
                return render(
                    request,
                    "line_modal.html",
                    {"create_form": create_form, "token": token, "assign_form": assign_form},
                )

        elif "assign_line" in request.POST:
            token = Token.objects.get(pk=token_id)
            assign_form = AssignLineSectionForm(request.POST, text_id=token.text.id)  # Reassign if POST
            if assign_form.is_valid():
                logger.debug("Assigning line to token")
                try:
                    section = assign_form.cleaned_data['identifier']
                    # Add the token to the section's tokens

                    # remove all the sections of type line that have been associated to this token
                    Section.objects.filter(text=token.text, type="line", tokens=token).delete()

                    # add the token to this section
                    section.tokens.add(token)

                    logger.debug(f"Section tokens: {section.tokens.all()}")
                    token.refresh_from_db()
                    # save the section
                    section.save()

                except Exception as e:
                    logger.error(f"Error adding token to line: {e}")
                    # refresh the token
                    token.refresh_from_db()
                    # check the relationship between the token and the line
                    logger.debug(f"Token: {token.section_tokens.all()}")
                # pass the data to line_data and then to line_update
                line_data = render_to_string("line_data.html", {"token": token})
                return render(
                    request,
                    "line_update.html",
                    {"line_data": line_data, "token_id": token_id},
                )

    if request.method == "GET":
        token = Token.objects.get(pk=token_id)
        create_form = CreateLineSectionForm()  # Initialize forms at the beginning
        assign_form = AssignLineSectionForm(text_id=token.text.id)

        return render(
            request,
            "line_modal.html",
            {"token": token, "create_form": create_form, "assign_form": assign_form},
        )
