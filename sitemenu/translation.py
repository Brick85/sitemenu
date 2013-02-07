from modeltranslation.translator import translator, TranslationOptions
from .sitemenu_settings import MENUCLASS
from . import import_item

Menu = import_item(MENUCLASS)

for model in [Menu]:
    if hasattr(model, '_translation_fields'):
        translation_option = type("{0}Translation".format(model.__name__), (TranslationOptions,), {
            'fields': model._translation_fields,
        })
        translator.register(model, translation_option)
