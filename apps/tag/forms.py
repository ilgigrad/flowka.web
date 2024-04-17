from tagulous.forms import TagField
from tagulous.models import TagOptions
from tag.models import TagSubject
from django import forms
from django.utils.translation import ugettext_lazy as _


class TagSearchForm(forms.Form):
    tags=TagField(
        required=False,
        tag_options=TagOptions(
            force_lowercase=True,
        ),
        autocomplete_tags=TagSubject.objects.autocomplete_most_frequent()
    )
    strict=forms.BooleanField(
        label = ('Strict Match'),
        required=False,
        label_suffix='',
        widget=forms.CheckboxInput(attrs={'id':'id_strict','class':'oi oi-check ml-0 my-1 mr-1 d-inline float-left' }))


class TagActionForm(forms.Form):
    tags=TagField(
        required=False,
        tag_options=TagOptions(
            force_lowercase=True,
        ),
        autocomplete_tags=TagSubject.objects.autocomplete_most_frequent()
    )
    strict=forms.BooleanField(
        label = ('Strict Match'),
        required=False,
        label_suffix='',
        widget=forms.HiddenInput(attrs={'id':'id_strict','name':'strict'}))

class TagForm(forms.Form):
    tags=TagField(
        required=False,
        tag_options=TagOptions(
            force_lowercase=True,
        ),
        autocomplete_tags=TagSubject.objects.autocomplete_most_frequent()
    )
