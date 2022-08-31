"""Adds language in manifest.json"""


from django.utils.translation import ugettext_lazy as _
from weblate.addons.events import EVENT_POST_ADD
from weblate.addons.scripts import BaseScriptAddon


class AddFoundryLanguage(BaseScriptAddon):
    """Add a new language entry in the manifest.json file when a new language is added."""

    # Event used to trigger the script
    events = (EVENT_POST_ADD,)
    # Name of the addon, has to be unique
    name = "weblate.foundryhub.add"
    # Verbose name and long descrption
    verbose = _("Add Foundry Hub language")
    description = _("Add a new language entry in the manifest.json file when a new language is added.")

    # Script to execute
    script = "/bin/true"
    # File to add in commit (for pre commit event)

    # does not have to be set
    add_file = "po/{{ language_code }}.po"