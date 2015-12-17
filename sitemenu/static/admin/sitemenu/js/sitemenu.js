(function($){
$(function() {

    var level_size = 25;
    var offset_margin = 7;

    $('#result_list tbody tr').each(function(){
        $('<div class="catcher_container"><span class="catcher catcher_before"><span></span></span><span class="catcher catcher_after"><span></span></span></div>').prependTo($('td', this)[0]);
    });

    var loader = $('<div id="loader"><span>Loading...</span><div></div></div>');
    $('body').append(loader);

    var save_position = {
        level: 0,
        target_id: 0,
        top_half: 0,
        element_id: 0
    };

    var target_level = 0;
    var target_element = null;
    var element = null;

    $(".drag_handle").draggable({
        helper: function(){
            return $('<div></div>');
        },
        start: function(event, ui) {
            $(this).closest('tbody').addClass('drag_started');
            element = $(this).closest('tr');
            save_position.element_id = get_id(element);
            element.addClass('dragging_element');
        },
        drag: function(event, ui) {
            set_level(ui.position.left);
        },
        stop: function(event, ui){
            $(this).closest('tbody').removeClass('drag_started');
            element.removeClass('dragging_element');
            element.css('opacity', '1.0');
        }
    });

    $( ".catcher" ).droppable({
        hoverClass: "ui-state-active",
        drop: function( event, ui ) {
            if(save_position.target_id != save_position.element_id){
                console.log(save_position);
                save();
            }
        },
        over: function( event, ui ) {

            var top_half = false;
            if($(this).hasClass('catcher_before')){
                top_half = true;
            }
            target_element = $(this).closest('tr');
            target_level = $('.result_list__ident_span', target_element).length;

            save_position.target_id = get_id(target_element);
            save_position.top_half = top_half?1:0;

            set_level(0);

            if(save_position.target_id != save_position.element_id){
                element.css('opacity', '0.5');
            } else {
                element.css('opacity', '1.0');
            }
        }
    });

    function get_id(el){
        return parseInt($('td.action-checkbox input', el).val(), 10);
    }

    function set_level(offset_left){
        level_add = 0;
        if(offset_left > 35 && save_position.top_half === 0) level_add++;
        save_position.level = target_level + level_add;

        catcher_span_left = save_position.level * level_size - offset_margin;
        $('#result_list tbody tr td .catcher span').css('left', catcher_span_left + 'px');
    }

    function save(){
        loader.show();
        $.ajax({
            type: "POST",
            url: save_url,
            data: save_position
        }).done(function( data ) {
            location.reload();
        });
    }
})})(django.jQuery);
