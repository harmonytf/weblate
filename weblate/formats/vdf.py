from typing import Callable, List, Optional, Tuple, Union

from django.core.exceptions import ValidationError
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from weblate.formats.ttkit import TTKitFormat, MonolingualSimpleUnit#, DictStoreMixin

vdfLanguageMapping = { # hardcoded in engine
    "en": "english",
    "de": "german",
    "fr": "french",
    "it": "italian",
    "ko": "korean",
    "es": "spanish",
    "es_MX": "mspanish",
    "zh_Hans": "schinese",
    "zh_Hant": "tchinese",
    "zh": "tchinese",
    "ru": "russian",
    "th": "thai",
    "ja": "japanese",
    "pt": "portuguese",
    "pl": "polish",
    "da": "danish",
    "nl": "dutch",
    "fi": "finnish",
    "no": "norwegian",
    "sv": "swedish",
    "cz": "czech",
    "hu": "hungarian",
    "ro": "romanian",
    "tr": "turkish",
}

class DictStoreMixin:
    @classmethod
    def validate_context(cls, context: str):
        id_class = cls.get_class().UnitClass.IdClass

        try:
            id_class.from_string(context)
        except Exception as error:
            raise ValidationError(gettext("Failed to parse the key: %s") % error)

class VDFFormat(DictStoreMixin, TTKitFormat):
    name = _("Valve VDF (Source Engine) localization file (UTF-8)")
    format_id = "valve_vdf"
    loader = ("vdf", "VDFFile")
    unit_class = MonolingualSimpleUnit
    autoload: Tuple[str, ...] = ("*_*.txt",)
    new_translation = """"lang"
{
	"Language" "english"
	"Tokens"
	{
	}
}
"""

    @staticmethod
    def mimetype():
        """Return most common media type for format."""
        return "text/plain"

    @staticmethod
    def extension():
        """Return most common file extension for format."""
        return "txt"

    @classmethod
    def get_language_full(cls, lang):
        code = str(lang)
        fallback = str(lang)
        if not isinstance(lang, str):
            code = lang.code
            fallback = lang.name.lower().replace(" ", "_")
        return vdfLanguageMapping[code] if code in vdfLanguageMapping else fallback

    @classmethod
    def get_language_filename(cls, mask: str, code: str) -> str:
        return mask.replace("*", cls.get_language_full(code))

    @classmethod
    def _get_new_file_content(cls, language):
        result = cls.new_translation
        if isinstance(result, str):
            result = result.replace('english', cls.get_language_full(language)).encode()
        return result

    @classmethod
    def create_new_file(
        cls,
        filename: str,
        language,
        base: str,
        callback: Optional[Callable] = None,
    ):
        """Handle creation of new translation file."""
        if base:
            # Parse file
            store = cls(base)
            if callback:
                callback(store)
            store.untranslate_store(language)
            store.store.savefile(filename)
        elif cls.new_translation is None:
            raise ValueError("Not supported")
        else:
            with open(filename, "wb") as output:
                output.write(cls._get_new_file_content(language)) # to insert language name where it belongs

class VDFFormatUTF16(VDFFormat):
    name = _("Valve VDF (Source Engine) localization file (UTF-16-LE)")
    format_id = "valve_vdf_utf16"
    loader = ("vdf", "VDFFileUTF16")

