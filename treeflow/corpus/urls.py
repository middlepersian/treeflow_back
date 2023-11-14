from django.urls import include, path, re_path
from treeflow.corpus.views.update_token import update_token
from treeflow.corpus.views.sections import sections_view
from treeflow.corpus.views.ud_editor import ud_editor
from treeflow.corpus.views.tokens import tokens_view
from treeflow.corpus.views.insert_after_token import insert_after_token_view
from treeflow.corpus.views.insert_before_token import insert_before_token_view
from treeflow.corpus.views.delete_token import delete_token_view
from treeflow.corpus.views.texts import texts_view
from treeflow.corpus.views.sections_editor import sections_editor_view

app_name = "treeflow.corpus"
urlpatterns = [
    path('update_token/', update_token, name='update_token'),
    path('sections/', sections_view, name='sections_view'),
    path('ud-editor/<uuid:section_id>/', ud_editor, name='ud_editor'), 
    path('tokens/', tokens_view, name='tokens'),
    path('texts/', texts_view, name='texts'),
    path('texts/<uuid:text_id>/sections/', sections_editor_view, name='sections-editor-view'),
    re_path(r'^tokens/(?P<token_id>[0-9a-f-]+)/insert_after/$', insert_after_token_view, name='insert_after_token'),
    re_path(r'^tokens/(?P<token_id>[0-9a-f-]+)/insert_before/$', insert_before_token_view, name='insert_before_token'),
    re_path(r'^tokens/(?P<token_id>[0-9a-f-]+)/delete/$', delete_token_view, name='delete_token'),
    ]