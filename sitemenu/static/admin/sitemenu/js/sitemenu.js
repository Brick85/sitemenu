$(function() {
    var drag_element = {};
    var level_size = 25;
    var fixed_margin = 25;
    var div_top = 2;

    var position_element = $('<div id="position_place"><div id="position_place_inner"></div></div>');

    var loader = $('<div id="loader"><div></div></div>');
    $('body').append(loader);

    var save_position = {};
    var save_on_drop = false;

    $("#result_list tbody tr").draggable({
        helper: function(){
            return $('<div></div>');
        },
        handle: '.drag_handle',
        start: function(event, ui) {
            drag_element = this;
        },
        stop: function(event, ui) {
            if(!save_on_drop)
                return;
            loader.show();
            $.ajax({
                type: "POST",
                url: save_url,
                data: save_position
            }).done(function( data ) {
                location.reload();
            });
        },
        drag: function(event, ui){
            save_on_drop = false;

            target_element = $(event.toElement).closest('tr.ui-draggable');
            drop_element = $(event.target).closest('tr.ui-draggable');

            drop_element.css('opacity', '1.0');

            target_id = get_id(target_element);
            if(typeof(target_id) == 'undefined'){
                position_element.hide();
                return;
            }
            drop_id = get_id(drop_element);
            if(target_id == drop_id){
                position_element.hide();
                return;
            }
            drop_element.css('opacity', '0.5');

            target_offset = target_element.offset();

            offsetX = event.pageX - parseInt(target_offset.left);
            offsetY = event.pageY - parseInt(target_offset.top);

            top_half = (drop_element.height()/2)>=offsetY;

            on_placeholder = $(event.toElement).attr('id') == 'position_place_inner';

            if(!on_placeholder){
                if(top_half){
                    $('div', position_element).css('top', (div_top-drop_element.height()) + 'px');
                } else {
                    $('div', position_element).css('top', div_top + 'px');
                }
            }

            position_element.show();

            target_level = $('.result_list__ident_span', target_element).length;

            move = Math.floor(ui.offset.left/level_size);
            if(top_half) // && get_id(target_element) == get_id($('#result_list tbody tr.ui-draggable:first-child')))
                move = 0;

            end_level = target_level + move;
            if(end_level<target_level) end_level = target_level;
            if(end_level>target_level+1) end_level = target_level+1;

            $(position_element).css('margin-left', (fixed_margin+level_size*end_level)+'px');

            $('td:first-child', target_element).append(position_element);

            save_position = {
                level: end_level,
                target_id: target_id,
                top_half: top_half?1:0,
                element_id: drop_id
            }
            save_on_drop = true;

        }
    });

    function get_id(el){
        return $('td.action-checkbox input', el).val()
    }
});
