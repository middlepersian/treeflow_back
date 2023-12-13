from django.shortcuts import render, get_object_or_404, Http404
from django.template.loader import render_to_string
from django.db import transaction
from treeflow.corpus.models import Dependency, Section, Source, Token, Text, Comment
from treeflow.images.models import Image
from treeflow.dict.models import Lemma, Sense
from treeflow.corpus.forms.comment_form import CommentFormSet
import logging

logger = logging.getLogger(__name__)


def comment_form(request, related_model_id=None):
    related_model_type = request.GET.get('related_model_type', None)
    logger.info("comments_form")
    logger.info(
        f"Related model type: {related_model_type}, ID: {related_model_id}")

    try:
        model_map = {
            'dependency': Dependency,
            'image': Image,
            'section': Section,
            'source': Source,
            'token': Token,
            'text': Text,
            'lemma': Lemma,
            'sense': Sense
        }

        model_class = model_map.get(related_model_type.lower(
        )) if related_model_id and related_model_type else None

        # Initialize the queryset based on the related model and ID
        if model_class:
            related_model = get_object_or_404(model_class, id=related_model_id)
            comments_queryset = Comment.objects.filter(
                **{f'{related_model_type.lower()}': related_model})
            logger.info(
                f"Comments filtered for {related_model_type}: {related_model_id}")
        else:
            comments_queryset = Comment.objects.none()
            logger.info("No filtering applied to comments queryset.")

        if request.method == 'POST':
            formset = CommentFormSet(request.POST, queryset=comments_queryset)
            if formset.is_valid():
                with transaction.atomic():
                    for form in formset:
                        if form.cleaned_data.get('DELETE', False) and form.instance.pk:
                            form.instance.delete()
                            logger.info(
                                f"Deleted Comment instance: {form.instance.pk}")
                        elif form.has_changed():
                            instance = form.save(commit=False)

                            setattr(
                                instance, related_model_type.lower(), related_model)
                            logger.info(
                                f"Assigning {related_model_type}: {related_model_id} to Comment instance")
                            # Assign user to the comment
                            instance.user = request.user
                            logger.info(
                                f"Assigning user: {request.user} to Comment instance")

                            instance.save()
                            logger.info(
                                f"Saved Comment instance: {instance} with ID: {instance.pk}")

                        else:
                            # log comments that are not changed
                            logger.info(
                                f"Skipping save for unchanged Comment instance: {form.instance.pk}")
                            logger.info(f"Form data: {form.cleaned_data}")

                logger.info("Comment formset saved successfully.")
                # Re-query the database to get the updated comments
                comments_queryset = Comment.objects.filter(**{f'{related_model_type.lower()}': related_model})
                logger.info(f"Refreshed comments queryset for {related_model_type}: {related_model_id}")

                # Prepare and return the response
                context = {
                    'related_model_type': related_model_type,
                    'related_model_id': related_model_id,
                    'comment_data': render_to_string('comment_data.html', {'comments': comments_queryset})
                }
                return render(request, 'comment_update.html', context)

            else:
                logger.error(
                    "Formset is not valid. Errors: {}".format(formset.errors))

        elif request.method == 'GET':
            # Handle GET request
            formset = CommentFormSet(queryset=comments_queryset)
            logger.info("Handling GET request")

            context = {'formset': formset, 'related_model_type': related_model_type,
                       'related_model_id': related_model_id}

            return render(request, 'comment_form.html', context)

    except Exception as e:
        logger.exception(f"Exception in comments_form: {e}")
        raise Http404(f"Error in comments_form: {str(e)}")
