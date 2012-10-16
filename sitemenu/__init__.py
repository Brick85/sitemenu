from django.utils import importlib


def import_item(path):
    try:
        render_import = path.split('.')
        render_module = importlib.import_module('.'.join(render_import[:-1]))
        render_function = render_import[-1]
    except ImportError, e:
        raise ImportError("Could not import function '%s': %s" % (path, e))
    try:
        func = getattr(render_module, render_function)
    except AttributeError, e:
        raise AttributeError("Could not find function '%s' in %s" % (render_function, render_module))
    return func
