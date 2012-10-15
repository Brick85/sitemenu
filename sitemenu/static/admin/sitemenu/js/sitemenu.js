$(function() {
    var drag_element = {};
    var level_size = 25;
    var fixed_margin = 25;
    // $("#result_list tbody").sortable({
    //     handle: '.drag_handle',
    //     placeholder: "ui-state-highlight",
    //     update: function( event, ui ){
    //         console.log(event)
    //     },
    //     sort: function( event, ui ){
    //         console.log(event.offsetX)
    //     }
    // }).disableSelection();

    var position_element = $('<tr class="position_element"><td><div></div></td></tr>');
    //var position_element_top = $('<tr class="position_element position_element_top"><td><div></div></td></tr>');
    //var position_element_bottom = $('<tr class="position_element position_element_bottom"><td><div></div></td></tr>');

    $("#result_list tbody tr").draggable({
        helper: function(){
            return $('<div></div>');
        },
        handle: '.drag_handle',
        start: function(event, ui) {
            drag_element = this;
            $(this).css('opacity', '0.5');
        },
        drag: function(event, ui){
            //$(event.toElement).css('border', '1px solid green');
            target_element = $(event.toElement).closest('tr.ui-draggable');
            drop_element = $(event.target);

            target_id = get_id(target_element);
            if(typeof(target_id) == 'undefined'){
                position_element.hide();
                return;
            }

            // if(target_id == get_id(drop_element)){
            //     position_element.hide();
            //     return;
            // }

            position_element.show();

            target_level = $('.result_list__ident_span', target_element).length;

            $('div', position_element).html(target_level + '; '+ target_id);
            console.log(event.offsetX, ui.offset.left);

            move = Math.floor(ui.offset.left/level_size);

            end_level = target_level + move;
            if(end_level<target_level) end_level = target_level;
            if(end_level>target_level+1) end_level = target_level+1;

            $('div', position_element).css('margin-left', (fixed_margin+level_size*end_level)+'px');

            top_half = (drop_element.height()/2)>=event.offsetY;
            if(top_half){
                position_element.insertBefore(target_element);
            } else {
                position_element.insertAfter(target_element);
            }
        }
    });

    $("#result_list tbody tr").droppable({
        drop: function(event, ui) {
            //console.log(event);
            drop_element = $(event.target);
            //console.log((drop_element.height()/2)>event.offsetY);
            $(drag_element).insertBefore(drop_element);
            $(drop_element).css('opacity', '1.0');
        },
        // over: function(event, ui) {
        //     position_element_top.insertBefore(this);
        //     position_element_bottom.insertAfter(this);
        // }
    });

    function get_id(el){
        return $('td.action-checkbox input', el).val()
    }
});
