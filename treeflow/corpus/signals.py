from django.db.models.signals import post_save
from django.dispatch import receiver
from treeflow.corpus.models import POS, Feature, Token, SectionToken

@receiver(post_save, sender=POS)
def update_section_on_pos_save(sender, instance, **kwargs):
    related_token = instance.token
    section_tokens = SectionToken.objects.filter(token=related_token)
    for st in section_tokens:
        related_section = st.section
        related_section.update_es_index()

@receiver(post_save, sender=Feature)
def update_section_on_feature_save(sender, instance, **kwargs):
    related_token = instance.token
    section_tokens = SectionToken.objects.filter(token=related_token)
    for st in section_tokens:
        related_section = st.section
        related_section.update_es_index()
