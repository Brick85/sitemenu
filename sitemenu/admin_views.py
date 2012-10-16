from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .sitemenu_settings import MENUCLASS
from . import import_item

Menu = import_item(MENUCLASS)

@staff_member_required
@csrf_exempt
def save_menu_position(request):
    ret = HttpResponse()
    try:
        element = Menu.objects.get(pk=request.POST['element_id'])
        target = Menu.objects.get(pk=request.POST['target_id'])
        level = int(request.POST['level'])
        top_half = True if int(request.POST['top_half']) == 1 else False
    except:
        messages.add_message(request, messages.ERROR, _('Unexpected error.'))
        return ret

    if target.level != level:
        same_level = False
    else:
        same_level = True

    position = ''
    if top_half:
        if same_level:
            real_target = target
            position = 'before'
        else:
            messages.add_message(request, messages.ERROR, _('Wrong position.'))
            return ret
    else:
        if same_level:
            real_target = target
            position = 'after'
        else:
            real_target = target

    if element.pk in real_target.get_parents_ids_list():
        messages.add_message(request, messages.WARNING, _('Impossible movement.'))
        return ret

    if same_level:
        items = Menu.objects.filter(parent=real_target.parent)
        a = 0
        for item in items:
            if item == element:
                continue
            if item == real_target and position == 'before':
                element.parent = item.parent
                element.sort = a
                a += 1
                element.save(skip_tree_update=True)
            item.sort = a
            a += 1
            item.save(skip_tree_update=True)
            if item == real_target and position == 'after':
                element.parent = item.parent
                element.sort = a
                a += 1
                element.save(skip_tree_update=True)
    else:
        items = Menu.objects.filter(parent=real_target.pk)
        element.parent = real_target
        element.sort = 0
        element.save(skip_tree_update=True)
        a = 1
        for item in items:
            if item == element:
                continue
            item.sort = a
            a += 1
            item.save(skip_tree_update=True)

    element.rebuild()

    messages.add_message(request, messages.SUCCESS, _('Item moved.'))

    return ret
