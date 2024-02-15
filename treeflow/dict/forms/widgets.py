from django_select2 import forms as s2forms

class SenseWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "sense__istartswith",
    ]
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({'style': 'width: 100%;'})
        super(SenseWidget, self).__init__(*args, **kwargs)



class LemmaWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "word__istartswith", 
    ]
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({'style': 'width: 100%;'})
        super(LemmaWidget, self).__init__(*args, **kwargs)
