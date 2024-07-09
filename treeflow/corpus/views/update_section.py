from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.forms import modelformset_factory
from django.db import transaction
import logging
from treeflow.corpus.models.section import Section
from treeflow.corpus.models.comment import Comment
from treeflow.corpus.forms.section_edit import SectionForm
from treeflow.corpus.forms.comment_section_form import CommentSectionForm

logger = logging.getLogger(__name__)

def update_section_view(request, section_id=None):
    section = get_object_or_404(Section, id=section_id)
    logger.info(f"Handling request for section ID: {section_id}")

    if request.method == "POST":
        form = SectionForm(request.POST, instance=section)
        CommentFormSet = modelformset_factory(Comment, form=CommentSectionForm, extra=0, can_delete=True)
        comment_formset = CommentFormSet(request.POST, queryset=Comment.objects.filter(section=section))

        if form.is_valid() and comment_formset.is_valid():
            with transaction.atomic():
                updated_section = form.save()

                comment_instances = comment_formset.save(commit=False)
                for comment in comment_instances:
                    comment.section = updated_section
                    comment.user = request.user
                    comment.save()

                # Handle deletions
                for form in comment_formset.deleted_forms:
                    if form.instance.pk:
                        form.instance.delete()

                comment_formset.save_m2m()
                return JsonResponse({"status": "success", "message": "Section and comments updated successfully"})
        else:
            errors = {**form.errors, **comment_formset.errors}
            logger.error(f"Errors during form validation: {errors}")
            return JsonResponse({"status": "error", "message": "Form validation failed", "errors": errors}, status=400)

    if request.method == "GET":
        form = SectionForm(instance=section)
        CommentFormSet = modelformset_factory(Comment, form=CommentSectionForm, extra=1, can_delete=True)
        comment_formset = CommentFormSet(queryset=Comment.objects.filter(section=section))
        context = {
            "form": form,
            "comment_formset": comment_formset,
            "section": section,
            "edit_mode": bool(section_id)
        }
        return render(request, "section_modal_update.html", context)
