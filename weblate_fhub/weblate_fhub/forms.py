

from weblate.addons.forms import BaseAddonForm
from django.utils.translation import gettext_lazy as _
from django import forms

class FoundryCustomizeForm(BaseAddonForm):
    manifest = forms.CharField(
        label=_("Path to manifest file relative to the repository root"),
        required=True,
        initial="module.json"
    )