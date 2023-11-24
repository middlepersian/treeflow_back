from django.urls import include, path, re_path
from treeflow.corpus.views.update_token import update_token
from treeflow.corpus.views.sections import sections_view
from treeflow.corpus.views.ud_editor import ud_editor, saveNewDependency, deleteDependency
from treeflow.corpus.views.tokens import tokens_view
from treeflow.corpus.views.insert_after_token import insert_after_token_view
from treeflow.corpus.views.insert_before_token import insert_before_token_view
from treeflow.corpus.views.delete_token import delete_token_view
from treeflow.corpus.views.texts import texts_view
from treeflow.corpus.views.update_pos_ajax import update_pos_ajax
from treeflow.corpus.views.sections_editor import sections_editor_view
from treeflow.corpus.views.get_sections import get_sections_by_type, get_child_sections, get_tokens_for_section
from treeflow.corpus.views.create_section import create_section_view
from treeflow.corpus.views.display_tokens import display_tokens_view
from treeflow.corpus.views.load_section_modal import load_section_modal

app_name = "treeflow.corpus"
urlpatterns = [
    path('update_token/<uuid:token_id>', update_token, name='update_token'),
    path('sections/', sections_view, name='sections_view'),
    path('ud-editor/<uuid:section_id>/', ud_editor, name='ud_editor'), 
    path('ud-editor/saveNewDependency/', saveNewDependency, name='saveDependency'), 
    path('ud-editor/deleteDependency/', deleteDependency, name='deleteDependency'), 
    path('tokens/', tokens_view, name='tokens'),
    path('texts/', texts_view, name='texts'),
    path('ajax/update_pos/', update_pos_ajax, name='update_pos_ajax'),  # The AJAX endpoint for updating POS
    path('texts/<uuid:text_id>/sections/', sections_editor_view, name='sections-editor-view'),
    path('get-sections/<uuid:text_id>/<str:section_type>/', get_sections_by_type, name='get_sections_by_type'),
    path('get-child-sections/<uuid:section_id>/', get_child_sections, name='get_child_sections'),
    path('get-tokens-for-section/<uuid:section_id>/', get_tokens_for_section, name='get_tokens_for_section'),
    path('create_section/', create_section_view, name='create_section'),
    path('display_tokens/', display_tokens_view, name='display_tokens'),
    path('load_section_modal/', load_section_modal, name='load_section_modal'),
    re_path(r'^tokens/(?P<token_id>[0-9a-f-]+)/insert_after/$', insert_after_token_view, name='insert_after_token'),
    re_path(r'^tokens/(?P<token_id>[0-9a-f-]+)/insert_before/$', insert_before_token_view, name='insert_before_token'),
    re_path(r'^tokens/(?P<token_id>[0-9a-f-]+)/delete/$', delete_token_view, name='delete_token'),
    ]
