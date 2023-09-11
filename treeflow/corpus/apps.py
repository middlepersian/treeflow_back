from django.apps import AppConfig


class CorpusAppConfig(AppConfig):
    name = 'treeflow.corpus'

    def ready(self):
        import treeflow.corpus.signals