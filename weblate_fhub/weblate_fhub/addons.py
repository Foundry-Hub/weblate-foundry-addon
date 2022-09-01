"""Adds language in manifest.json"""

import os, json, uuid, io

from django.utils.translation import gettext_lazy as _, gettext, activate, deactivate
from weblate.addons.events import EVENT_POST_ADD
from weblate.addons.scripts import BaseScriptAddon
from weblate.trans.models import translation
from weblate_fhub.forms import FoundryCustomizeForm

class AddFoundryLanguage(BaseScriptAddon):
    """Add a new language entry in the manifest file when a new language is added."""

    # Event used to trigger the script
    events = (EVENT_POST_ADD,)
    # Name of the addon, has to be unique
    name = "weblate.foundryhub.foundryhub"
    # Verbose name and long descrption
    verbose = _("Foundry VTT Integration")
    description = _("Add a new language entry in the manifest.json file when a new language is added.")

    settings_form = FoundryCustomizeForm
    
    def post_add(self, translation: translation):
        config = self.instance.configuration
        manifest = config.get("manifest", "module.json")

        if translation:
            component = translation.component

        if component.is_repo_link:
            target = component.linked_component
        else:
            target = component

        # These languages needs to be converted to their FVTT code
        foundryvtt_code = {
            "zh-rTW" : "zh-TW",
            "pt" : "pt-BR",
            "zh-rCN" : "cn"
        }

        new_code = translation.language_code

        if new_code in foundryvtt_code:
            new_code = foundryvtt_code[new_code]

        activate(translation.language_code)
        new_name = gettext(translation.language.name)
        deactivate()

        manifest_fullpath = target.full_path + "/" + manifest

        with io.open(manifest_fullpath, mode='r', encoding='utf-8') as f:
            manifest_obj = json.load(f)
            src_path = manifest_obj['languages'][0]['path']

            manifest_obj['languages'].append({
                "lang": new_code,
                "name": new_name,
                "path": os.path.dirname(src_path) + "/" + os.path.basename(translation.filename)
            })

        tempfile = os.path.join(os.path.dirname(manifest_fullpath), str(uuid.uuid4()))
        with io.open(tempfile, mode='w', encoding='utf-8') as f:
            json.dump(manifest_obj, f, indent=4, ensure_ascii=False)

        os.replace(tempfile, manifest_fullpath)
        return