from django import forms
from treeflow.corpus.models.comment import Comment

class CommentSectionForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'user']  # Include user to handle it in the form, but it will be set automatically

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract user from kwargs and remove it
        super(CommentSectionForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['user'].widget = forms.HiddenInput()  # Hide the user field
        self.fields['comment'].widget = forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your comment here...'})

    def save(self, commit=True):
        instance = super(CommentSectionForm, self).save(commit=False)
        if not instance.user_id:  # Set user only if it's not already set
            instance.user = self.user
        if commit:
            instance.save()
        return instance