from json import JSONEncoder


# patch the json module so that it checks models for a 'to_json' method
# and invokes that if found
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default
