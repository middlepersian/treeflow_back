from django.shortcuts import render
from treeflow.corpus.models.comment import Comment
from treeflow.corpus.forms.comment_form import CommentFormSet

def comments_view(request, related_model_id):
    if request.method == 'POST':
        formset = CommentFormSet(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.token_id = related_model_id  # Set the foreign key field
                instance.save()
            # Redirect or show a success message
            # For example: return redirect('some-view-name')
    else:
        formset = CommentFormSet(queryset=Comment.objects.none())
        for form in formset:
            form.fields['related_model_id'].initial = related_model_id

    return render(request, 'comment_form_modal.html', {'formset': formset})
