import re

from django.utils.translation import gettext_lazy as _

from weblate.checks.base import TargetCheck

SOURCE_ENGINE_COLOR_REGEX = re.compile(r'\^(?P<color>[0-9A-F]{8})')
SOURCE_ENGINE_PARAM_REGEX = re.compile(r'(?P<param>%s[0-9]{1})')
SOURCE_ENGINE_BUTTON_REGEX = re.compile(r'(?P<btn>%\[[A-Z_\|]+\]%)')
SOURCE_ENGINE_BIND_REGEX = re.compile(r'(?P<bind>%(?!s[0-9])[A-Za-z0-9_+\-]+%)')
SOURCE_ENGINE_RUI_REGEX = re.compile(r'(?P<rui>%\$(?:rui|vgui)[A-Za-z0-9_/\\]+%)')
SOURCE_ENGINE_R2_FONT_STYLE_REGEX = re.compile(r'(?P<fontstyle>`[0-9]{1})')

class BaseStatsCheck(TargetCheck):
    stats_check_regex = "INVALID"
    stats_check_group_name = "INVALID"
    stats_check_case_insensitive = False

    def string_to_stats(self, string: str, regex: re.Pattern[str], group_name: str, case_insensitive: bool = False):
        stats = {}
        for x in re.finditer(regex, string):
            item = x.group(group_name)
            if case_insensitive:
                item = item.upper()
            if not (item in stats):
                stats[item] = 0
            stats[item] += 1
        return stats

    # return True if failed
    def check_single(self, source, target, unit):
        stats_source = self.string_to_stats(source, self.stats_check_regex, self.stats_check_group_name, self.stats_check_case_insensitive)
        stats_target = self.string_to_stats(target, self.stats_check_regex, self.stats_check_group_name, self.stats_check_case_insensitive)

        for x in stats_source:
            if not (x in stats_target):
                return True
            if stats_source[x] != stats_target[x]:
                return True
        for x in stats_target:
            if not (x in stats_source):
                return True
            if stats_target[x] != stats_source[x]:
                return True

        return False

class MatchingColors(BaseStatsCheck):
    """Check Source Engine colors like ^ABCDEF00."""

    check_id = "source_engine_matching_colors"
    name = _("Matching colors (Source Engine)")
    description = _("Source and translation have a mismatch of color codes used among them")

    stats_check_regex = SOURCE_ENGINE_COLOR_REGEX
    stats_check_group_name = "color"
    stats_check_case_insensitive = False

class MatchingParams(BaseStatsCheck):
    """Check Source Engine string parameters like %s1."""

    check_id = "source_engine_matching_params"
    name = _("Matching parameters (Source Engine)")
    description = _("Source and translation have a mismatch of parameters used among them")

    stats_check_regex = SOURCE_ENGINE_PARAM_REGEX
    stats_check_group_name = "param"
    stats_check_case_insensitive = False

class MatchingButtons(BaseStatsCheck):
    """Check Source Engine button codes like %[A_BUTTON]% or %[A_BUTTON|ENTER]%."""

    check_id = "source_engine_matching_buttons"
    name = _("Matching buttons (Source Engine)")
    description = _("Source and translation have a mismatch of button codes used among them")

    stats_check_regex = SOURCE_ENGINE_BUTTON_REGEX
    stats_check_group_name = "btn"
    stats_check_case_insensitive = False

class MatchingBinds(BaseStatsCheck):
    """Check Source Engine bind codes like %weaponPickup%."""

    check_id = "source_engine_matching_binds"
    name = _("Matching binds (Source Engine)")
    description = _("Source and translation have a mismatch of bind codes used among them")

    stats_check_regex = SOURCE_ENGINE_BIND_REGEX
    stats_check_group_name = "bind"
    stats_check_case_insensitive = True

class MatchingRUI(BaseStatsCheck):
    """Check Titanfall 2 RUI embed codes like %$rui/hud/titan_core%."""

    check_id = "source_engine_matching_r2_rui"
    name = _("Matching RUI embeds (Titanfall 2)")
    description = _("Source and translation have a mismatch of Titanfall 2 RUI codes used among them")

    stats_check_regex = SOURCE_ENGINE_RUI_REGEX
    stats_check_group_name = "rui"
    stats_check_case_insensitive = False

class MatchingR2FontStyle(BaseStatsCheck):
    """Check Source Engine Titanfall 2 font styles like `1, `2, `3."""

    check_id = "source_engine_matching_r2_font_style"
    name = _("Matching font styles (Titanfall 2)")
    description = _("Source and translation have a mismatch of Titanfall 2 font style codes used among them")

    stats_check_regex = SOURCE_ENGINE_R2_FONT_STYLE_REGEX
    stats_check_group_name = "fontstyle"
    stats_check_case_insensitive = False
