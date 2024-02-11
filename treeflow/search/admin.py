from django.contrib import admin
from .models import SearchSession, SearchCriteria, ResultFilter

# Register your models here.
admin.site.register(SearchCriteria)
admin.site.register(SearchSession)
admin.site.register(ResultFilter)