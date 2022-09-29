import re

from django.utils.translation import gettext_lazy as _

from weblate.checks.base import CountingCheck, TargetCheck, TargetCheckParametrized

SOURCE_ENGINE_COLOR_REGEX = re.compile(r'\^(?P<color>[0-9A-F]{8})')
SOURCE_ENGINE_PARAM_REGEX = re.compile(r'(?P<param>%s[0-9]{1})')

class MatchingColors(TargetCheck):
    """Check Source Engine colors like ^ABCDEF00."""

    check_id = "source_engine_matching_colors"
    name = _("Matching colors (Source Engine)")
    description = _("Source and translation have a mismatch of color codes used among them")

    def string_to_color_stats(self, string: str):
        colors = {}
        for x in re.finditer(SOURCE_ENGINE_COLOR_REGEX, string):
            color = x.group("color")
            if not (color in colors):
                colors[color] = 0
            colors[color] += 1
        return colors

    # return True if failed
    def check_single(self, source, target, unit):
        colors_source = self.string_to_color_stats(source)
        colors_target = self.string_to_color_stats(target)

        for x in colors_source:
            if not (x in colors_target):
                return True
            if colors_source[x] != colors_target[x]:
                return True
        for x in colors_target:
            if not (x in colors_source):
                return True
            if colors_target[x] != colors_source[x]:
                return True

        return False

class MatchingParams(TargetCheck):
    """Check Source Engine string parameters like %s1."""

    check_id = "source_engine_matching_params"
    name = _("Matching parameters (Source Engine)")
    description = _("Source and translation have a mismatch of color codes used among them")

    def string_to_param_stats(self, string: str):
        params = {}
        for x in re.finditer(SOURCE_ENGINE_PARAM_REGEX, string):
            param = x.group("param")
            if not (param in params):
                params[param] = 0
            params[param] += 1
        return params

    # return True if failed
    def check_single(self, source, target, unit):
        params_source = self.string_to_param_stats(source)
        params_target = self.string_to_param_stats(target)

        for x in params_source:
            if not (x in params_target):
                return True
            if params_source[x] != params_target[x]:
                return True
        for x in params_target:
            if not (x in params_source):
                return True
            if params_target[x] != params_source[x]:
                return True

        return False
