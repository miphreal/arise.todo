def get_storage(name=None, options=None):
    from .conf import STORAGES, DEFAULT_STORAGE
    if name and name not in STORAGES:
        raise KeyError('{} storage does not exist'.format(name))

    options = options or {}

    if name:
        return STORAGES[name](**options)
    else:
        storage_class = STORAGES[DEFAULT_STORAGE['name']]
        return storage_class(**dict(DEFAULT_STORAGE['options'], **options))
