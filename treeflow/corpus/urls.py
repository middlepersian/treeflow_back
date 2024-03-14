from django.urls import include, path, re_path
from treeflow.corpus.views.update_token import update_token
from treeflow.corpus.views.update_text import update_text
from treeflow.corpus.views.ud_editor import ud_editor, saveNewDependency, deleteDependency, setNewRoot
from treeflow.corpus.views.tokens import tokens_view
from treeflow.corpus.views.insert_after_token import insert_after_token_view
from treeflow.corpus.views.insert_before_token import insert_before_token_view
from treeflow.corpus.views.delete_token import delete_token_view
from treeflow.corpus.views.texts import texts_view
from treeflow.corpus.views.sections import sections_view
from treeflow.corpus.views.get_sections import get_sections_by_type, get_child_sections, get_tokens_for_section
from treeflow.corpus.views.create_section import create_section_view
from treeflow.corpus.views.section_editor import section_editor_form_view
from treeflow.corpus.views.save_section import save_section_view
from treeflow.corpus.views.display_tokens import display_tokens_view
from treeflow.corpus.views.load_section_modal import load_section_modal
from treeflow.corpus.views.get_feature_formset import get_feature_formset
from treeflow.corpus.views.pos_feature_form import pos_feature_form
from treeflow.corpus.views.bib_edit import BibEntryListView, BibEntryCreateView
from treeflow.corpus.views.get_feature_formset import get_feature_formset
from treeflow.corpus.views.pos_feature_form import pos_feature_form
from treeflow.corpus.views.sentence import sentence_view
from treeflow.corpus.views.sentences import sentences_view
from treeflow.corpus.views.bib_edit import BibEntryCreateView
from treeflow.corpus.views.bibentry import BibEntryListView, BibEntryDetailView
from treeflow.corpus.views.comment_form import comment_form
from treeflow.corpus.views.sources import SourceTableView, source_manuscripts , SourceUpdateView, SourceDeleteView, create_source, add_related_source, add_related_bib, sources
from treeflow.corpus.views.dropdown_redirect import dropdown_redirect
from treeflow.corpus.views.update_source import update_source
from treeflow.corpus.views.token_lemma_sense import token_lemma_sense_view
from treeflow.corpus.views.save_token import save_token
from treeflow.corpus.views.manuscripts import manuscripts, get_images_for_manuscript, get_images_for_manuscript_table
from treeflow.corpus.views.export_text import resolve_sentence, resolve_text
from treeflow.corpus.views.openseadragon import openseadragon, imageSelector, sourceSelector

app_name = "treeflow.corpus"
urlpatterns = [
    path('update_token/<uuid:token_id>', update_token, name='update_token'),
    path('update_source/<uuid:source_id>', update_source, name='api_update_source'),
    path('update_text/<uuid:text_id>/', update_text, name='update_text'),
    path('ud-editor/<uuid:section_id>/', ud_editor, name='ud_editor'), 
    path('ud-editor/saveNewDependency/', saveNewDependency, name='saveDependency'), 
    path('ud-editor/deleteDependency/', deleteDependency, name='deleteDependency'),
    path('ud-editor/setNewRoot/', setNewRoot, name='setNewRoot'),
    path('texts/', texts_view, name='texts'),
    path('tokens/<uuid:text_id>', tokens_view, name='tokens'),
    path('tokens/<uuid:text_id>/<uuid:section_id>', tokens_view, name='tokens'),
    path('sentence/<uuid:sentence_id>', sentence_view, name='sentence'),
    path('sentences/<uuid:text_id>', sentences_view, name='sentences'),
    path('sections/<uuid:text_id>', sections_view, name='sections'),
    path('section/', section_editor_form_view, name='section'),
    path('section/<uuid:section_id>', section_editor_form_view, name='section'),
    path('save_section/', save_section_view, name='save_section'),
    path('save_section/<uuid:section_id>', save_section_view, name='save_section'),
    path('dropdown_redirect/', dropdown_redirect, name='dropdown_redirect'),
    path('get-sections/<uuid:text_id>/<str:section_type>/', get_sections_by_type, name='get_sections_by_type'),
    path('get-child-sections/<uuid:section_id>/', get_child_sections, name='get_child_sections'),
    path('get-tokens-for-section/<uuid:section_id>/', get_tokens_for_section, name='get_tokens_for_section'),
    path('get-feature-formset/<uuid:token_id>/', get_feature_formset, name='get_feature_formset'),
    path('create_section/', create_section_view, name='create_section'),
    path('display_tokens/', display_tokens_view, name='display_tokens'),
    path('load_section_modal/', load_section_modal, name='load_section_modal'),
    path('bibliography/create/', BibEntryCreateView.as_view(), name='bibliography-create'),
    path('pos_feature_form/<uuid:token_id>/', pos_feature_form, name='pos_feature_form'),
    path('bibliography/', BibEntryListView.as_view(), name='bibliography'),
    path('bibliography/<uuid:bibEntry_id>/', BibEntryDetailView.as_view(), name='bibliography-detail'),
    path('bibliography/create/', BibEntryCreateView.as_view(), name='bibliography-create'),
    path('comment_form/<uuid:related_model_id>/', comment_form, name='comment_form'),    
    path('sources/',sources, name='sources'),
    path('sources/edit/<uuid:source_id>/', SourceUpdateView.as_view(), name='update_source'),
    path('sources/delete/<uuid:source_id>/', SourceDeleteView.as_view(), name='source_delete'),
    path('sources/add/', create_source, name='source_add'),
    path('sources/add_related_source/<uuid:source_id>/', add_related_source, name='add_related_source'),
    path('sources/add_related_bib/<uuid:source_id>/', add_related_bib, name='add_related_bib'),
    path('sources/manuscripts/', source_manuscripts, name='manuscripts'),
    path('token_lemma_sense/<uuid:token_id>/', token_lemma_sense_view, name='token_lemma_sense'),
    path('save_token/<uuid:token_id>/', save_token, name='save_token'),
    path('manuscripts/', manuscripts, name='manuscripts'),
    path('manuscript/<uuid:manuscript_id>/images',get_images_for_manuscript,name='manuscript_images'),
    path('manuscript/<uuid:manuscript_id>/images/table',get_images_for_manuscript_table,name='manuscript_images_table'),
    path('export/sentence/<uuid:section_id>',resolve_sentence,name='export_sentence'),
    path('export/text/<uuid:text_id>',resolve_text,name='export_sentence'),

    path('openseadragon/', sourceSelector, name='sourceSelector'),
    path('openseadragon/imageSelect/', imageSelector, name='imageSelector'),
    path('openseadragon/viewer/', openseadragon, name='imageViewer'),
    re_path(r'^tokens/(?P<token_id>[0-9a-f-]+)/insert_after/$', insert_after_token_view, name='insert_after_token'),
    re_path(r'^tokens/(?P<token_id>[0-9a-f-]+)/insert_before/$', insert_before_token_view, name='insert_before_token'),
    re_path(r'^tokens/(?P<token_id>[0-9a-f-]+)/delete/$', delete_token_view, name='delete_token'),
    ]

