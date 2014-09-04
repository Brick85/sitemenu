from django.core.management.base import BaseCommand
from optparse import make_option
import json
from sitemenu.sitemenu_settings import MENUCLASS
from sitemenu import import_item
from django.utils.text import slugify
Menu = import_item(MENUCLASS)
from transliterate import translit
from django.utils import translation

# transliterate required

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-f", "--file", dest="filename", help="read JSON file", metavar="FILE"),
    )

    def handle(self, *args, **options):
        # Menu.objects.all()[0].rebuild()
        # return
        translation.activate('ru')
        if not options['filename']:
            self.stdout.write("No JSON file supplied")
            self.stdout.write("-f filename.json")
            self.stdout.write("File format:")
            self.stdout.write("""[
    {
        "parent": [int or null],
        "categories": [
            {
                "title": "title 1",
                "page_type": "prod",
                "categories": [
                    {
                        "title": "title 1.1",
                        "page_type": "prod"
                    },
                    ...
                ]
            },
            {
                "title": "title 2",
                "page_type": "prod"
            },
            ...
        ]
    },
...
]
""")

            return
        f = open(options['filename'])
        #print f.read()
        data = json.load(f)
        f.close()
        for root_cat in data:
            if root_cat['parent'] != None:
                parent = Menu.objects.get(pk=root_cat['parent'])
            else:
                parent = None
            self.create_categories(parent, root_cat['categories'])

        # Menu.objects.all()[0].rebuild()
        # return

    def create_categories(self, parent, categories):
        print "Creating for:", parent
        for i, c in enumerate(categories):
            m = Menu()
            m.parent = parent
            m.page_type = c['page_type']
            m.title = c['title']
            m.title_ru = c['title']
            m.title_en = translit(c['title'], reversed=True)
            m.enabled = True
            m.url = slugify(translit(c['title'], reversed=True))
            m.save()
            print "created:", m
            if 'categories' in c:
                self.create_categories(m, c['categories'])

