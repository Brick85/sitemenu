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

__If you need customized fields:__

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

Server Cache
------------

create servercache.py:

```python
from qshop.cart import Cart

def get_servercache_str(request, response):
    argsstr = ''

    cart = Cart(request)
    products_in_cart = cart.total_products_with_qty()
    if products_in_cart > 0:
        argsstr += 'p{0}'.format(products_in_cart)

    return argsstr
```

add as first middleware:

```python
    'sitemenu.middleware.ServerCacheMiddleware',
```

add to settings.py

```python
SITEMENU_SERVER_CACHE_DIR = rel('_server_cache')
SITEMENU_SERVER_CACHE_ARGS_FUNC = 'path_to.servercache.get_servercache_str'
```

add to any models.py

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from sitemenu import sitemenu_settings

from django.contrib.sessions.models import Session
from qshop.cart.models import Cart, Item
import shutil

if sitemenu_settings.SERVER_CACHE_DIR:
    skip_save_classes = (Session, Cart, Item)

    @receiver(post_save)
    def clear_cache_after_save(sender, **kwargs):
        if not isinstance(kwargs['instance'], skip_save_classes):
            shutil.rmtree(sitemenu_settings.SERVER_CACHE_DIR, True)
```

add to nginx vhost

```
    location / {
        root /path_to/_server_cache;
        try_files "${uri}cache${cookie_scas}${args}.html" @django;
    }

    location @django {
        ...
    }
```
