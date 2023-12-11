from django.shortcuts import render, Http404
from treeflow.corpus.models import Dependency, Section, Source, Token, Text, Comment
from treeflow.images.models import Image
from treeflow.dict.models import Lemma, Sense
from treeflow.corpus.forms.comment_form import CommentFormSet
import logging

logger = logging.getLogger(__name__)

def comment_form(request, related_model_type=None, related_model_id=None):
    logger.info("comments_form")
    logger.info(f"Related model type: {related_model_type}, ID: {related_model_id}")

    try:
        if related_model_id and related_model_type:
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

            model_class = model_map.get(related_model_type.lower())
            if model_class and model_class.objects.filter(id=related_model_id).exists():
                comments_queryset = Comment.objects.filter(**{f'{related_model_type.lower()}': related_model_id})
            else:
                logger.warning(f"Model type {related_model_type} with ID {related_model_id} does not exist.")
                comments_queryset = Comment.objects.none()
        else:
            comments_queryset = Comment.objects.none()

        formset = CommentFormSet(request.POST or None, queryset=comments_queryset)

        if request.method == 'POST':
            logger.info("POST request received")
            formset = CommentFormSet(request.POST, request.FILES, queryset=comments_queryset)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    if related_model_id and related_model_type:
                        setattr(instance, f'{related_model_type.lower()}_id', related_model_id)
                    instance.save()
            else:
                logger.info(f"Formset errors: {formset.errors}")
        else:
            logger.info("Handling GET request")

        context = {'formset': formset, 'related_model_type': related_model_type, 'related_model_id': related_model_id}
        return render(request, 'comment_form.html', context)
    except Exception as e:
        logger.exception(e)
        raise Http404(f"Error in comments_form: {str(e)}")
