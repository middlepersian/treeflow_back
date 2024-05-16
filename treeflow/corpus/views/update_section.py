from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.forms import modelformset_factory
from django.db import transaction
import logging
from treeflow.corpus.models.section import Section
from treeflow.corpus.models.comment import Comment
from treeflow.corpus.forms.section_edit_display_tokens import SectionForm
from treeflow.corpus.forms.comment_section_form import CommentSectionForm


logger = logging.getLogger(__name__)

def update_section_view(request, section_id=None):
    section = get_object_or_404(Section, id=section_id) if section_id else None
    logger.info(f"Handling request for section ID: {section_id}")

    if request.method == "POST":
        form = SectionForm(request.POST, instance=section)
        CommentFormSet = modelformset_factory(Comment, form=CommentSectionForm, extra=0, can_delete=True)
        comment_formset = CommentFormSet(request.POST, queryset=Comment.objects.none())

        logger.info("Processing POST request...")
        if form.is_valid() and comment_formset.is_valid():
            with transaction.atomic():
                updated_section = form.save()
                logger.info(f"Section {updated_section.id} saved successfully.")
                
                comment_instances = comment_formset.save(commit=False)
                for comment in comment_instances:
                    comment.section = updated_section
                    comment.user = request.user
                    comment.save()
                    logger.info(f"Comment {comment.id} linked to section {updated_section.id} and saved.")
                
                comment_formset.save_m2m()
                logger.info("All comments updated successfully with section.")
                return JsonResponse({"status": "success", "message": "Section and comments updated successfully"})
        else:
            errors = {**form.errors, **comment_formset.errors}
            logger.error(f"Errors during form validation: {errors}")
            return JsonResponse({"status": "error", "message": "Form validation failed", "errors": errors}, status=400)

    else:  # GET request
        form = SectionForm(instance=section)
        CommentFormSet = modelformset_factory(Comment, form=CommentSectionForm, extra=1, can_delete=True)
        comment_formset = CommentFormSet(queryset=Comment.objects.filter(section=section))

        logger.info(f"Loaded {comment_formset.queryset.count()} comments for section {section_id}.")
        if section:
            logger.info(f"Section loaded: {section.title}")  # Assuming 'title' is a field in your Section model
        else:
            logger.warning(f"No section found with ID: {section_id}")

        context = {
            "form": form,
            "comment_formset": comment_formset,
            "section": section,
            "edit_mode": bool(section_id)
        }
        return render(request, "section_modal.html", context)