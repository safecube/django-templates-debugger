from django.conf import settings
from django.test.signals import setting_changed

USER_SETTINGS = getattr(settings, "TEMPLATES_DEBUGGER", None)

DEFAULTS = {
    "MATCH_PATH": "*",
}

# List of settings that cannot be empty
MANDATORY = []


class TemplateDebuggerSettings:
    def __init__(self, user_settings=None, defaults=None):
        self._user_settings = user_settings or {}
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "TEMPLATES_DEBUGGER", {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid TemplateDebugger setting: %s" % attr)
        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()


app_settings = TemplateDebuggerSettings(USER_SETTINGS, DEFAULTS)


def reload_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "TEMPLATES_DEBUGGER":
        app_settings.reload()


setting_changed.connect(reload_settings)
