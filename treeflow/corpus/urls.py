from django.urls import path, re_path
from treeflow.corpus.views.update_token import update_token
from treeflow.corpus.views.update_text import update_text
from treeflow.corpus.views.update_section import update_section_view
from treeflow.corpus.views.update_section_token import update_section_token_view
from treeflow.corpus.views.ud_editor import ud_editor, saveNewDependency, deleteDependency, setNewRoot
from treeflow.corpus.views.tokens import tokens_view
from treeflow.corpus.views.insert_after_token import insert_after_token_view
from treeflow.corpus.views.insert_before_token import insert_before_token_view
from treeflow.corpus.views.delete_token import delete_token_view
from treeflow.corpus.views.delete_section import delete_section_view
from treeflow.corpus.views.texts import texts_view
from treeflow.corpus.views.sections import sections_view
from treeflow.corpus.views.get_sections import get_sections_by_type, get_tokens_for_section, get_section_data
from treeflow.corpus.views.get_images import get_images_view
from treeflow.corpus.views.create_section import create_section_view
from treeflow.corpus.views.section_editor import section_editor_form_view
from treeflow.corpus.views.save_section import save_section_view
from treeflow.corpus.views.display_tokens import display_tokens_view
from treeflow.corpus.views.load_section_modal_create import load_section_modal_create
from treeflow.corpus.views.load_section_modal_update import load_section_modal_update
from treeflow.corpus.views.line_form import line_form_view
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
from treeflow.corpus.views.sources import source_manuscripts , SourceUpdateView, SourceDeleteView, create_source, add_related_source, add_related_bib, sources
from treeflow.corpus.views.dropdown_redirect import dropdown_redirect
from treeflow.corpus.views.update_source import update_source
from treeflow.corpus.views.token_lemma_sense import token_lemma_sense_view
from treeflow.corpus.views.save_token import save_token
from treeflow.corpus.views.manuscripts import manuscripts, get_images_for_manuscript, get_images_for_manuscript_table
from treeflow.corpus.views.export_text import  download_text_mpft, resolve_state_mpft, download_text_conllu, resolve_state_conllu
from treeflow.corpus.views.openseadragon import openseadragon, imageSelector


app_name = "treeflow.corpus"
urlpatterns = [
    path('delete_section/<uuid:section_id>/', delete_section_view, name='delete_section'),
    path('update_section/<uuid:section_id>/', update_section_view, name='update_section'),
    path('update_section_token/<uuid:token_id>/', update_section_token_view, name='update_section_token'),
    path('update_source/<uuid:source_id>/', update_source, name='api_update_source'),
    path('update_text/<uuid:text_id>/', update_text, name='update_text'),
    path('update_token/<uuid:token_id>', update_token, name='update_token'),
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
    path('create_section/', create_section_view, name='create_section'),
    path('save_section/', save_section_view, name='save_section'),
    path('save_section/<uuid:section_id>', save_section_view, name='save_section'),
    path('dropdown_redirect/', dropdown_redirect, name='dropdown_redirect'),
    path('get-sections-by-type/', get_sections_by_type, name='get_sections_by_type'),
    path('get-section-data/<uuid:section_id>/', get_section_data, name='get_section_data'),
    path('get-tokens-for-section/<uuid:section_id>/', get_tokens_for_section, name='get_tokens_for_section'),
    path('get-feature-formset/<uuid:token_id>/', get_feature_formset, name='get_feature_formset'),
    path('get-images/', get_images_view, name='get_images'),
    path('display_tokens/', display_tokens_view, name='display_tokens'),
    path('load_section_modal_create/', load_section_modal_create, name='load_section_modal_create'),
    path('load_section_modal_update/', load_section_modal_update, name='load_section_modal_update'),
    path('line-form/<uuid:token_id>/', line_form_view, name='line_form'),  
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
    path('export/text/mptf/<uuid:text_id>',download_text_mpft,name='mptf'),
    path('export/text/conllu/<uuid:text_id>',download_text_conllu,name='conllu'),
    path('status/text/mptf/<uuid:text_id>',resolve_state_mpft,name='mptf_state'),
    path('status/text/conllu/<uuid:text_id>',resolve_state_conllu,name='conllu_state'),
    path('openseadragon/imageSelect/', imageSelector, name='imageSelector'),
    path('openseadragon/viewer/', openseadragon, name='imageViewer'),
    re_path(r'^tokens/(?P<token_id>[0-9a-f-]+)/insert_after/$', insert_after_token_view, name='insert_after_token'),
    re_path(r'^tokens/(?P<token_id>[0-9a-f-]+)/insert_before/$', insert_before_token_view, name='insert_before_token'),
    re_path(r'^tokens/(?P<token_id>[0-9a-f-]+)/delete/$', delete_token_view, name='delete_token'),
    ]

