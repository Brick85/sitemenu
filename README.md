Django-SiteMenu
===============

Nested menu for django projects. Without MPTT and with drag'n'drop sorting.
Easy customizable. Looks like simple model for using.

Features
--------
- Customazible menu fields
- Drag'n'drop sorting
- Template tags for menu rendering and breadcrumbs
- One select for menu tree output
- Additional parameters after urls

Installation
------------
- Install django-sitemenu from here or from PyPi: pip install django-sitemenu
- Add "django.core.context_processors.request" to TEMPLATE_CONTEXT_PROCESSORS
- Add "sitemenu" to INSTALLED_APPS
- Add "url(r'^', include('sitemenu.urls'))" to your urls.py
- Run 'manage.py syncdb' to create table

You can use this code to add context proccessor:

```python
from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
)
```

If you need customized fields:

Create new app

Create model in models.py

```python
from sitemenu.models import SiteMenu
class Menu(SiteMenu):
    # your additional fields
```
In settings.py set SITEMENU_MENUCLASS to 'your_app.models.Menu'

And register it in admin

```python
from django.contrib import admin
from sitemenu.admin import SiteMenuAdmin
from your_app.models import Menu
admin.site.register(Menu, SiteMenuAdmin)
```

Configuration
-------------
If you need your own views and page types (probably you will need):
Define in settings.py SITEMENU_PAGES with tupe:

```python
(
    ('text', 'Text page',     'sitemenu.views.render_menupage'),
    ('redr', 'Redirect page', 'sitemenu.views.render_redirectpage'),
    ('indx', 'Index page',    'sitemenu.views.render_menupage'),
)
```

- First column is type id and must be 4 chars length.
- Second is template name.
- Third is path to your view. It must accept 3 args: request, menu, url_add
  - request is request
  - menu is instance of current class
  - url_add is list of additional urls passed to your view. If you have url like /my/view/ and user accessing /my/view/add1/add2/ and /my/view/ doesn't have child with url add1, then ['add1', 'add2'] will be passed to your view as url_add
