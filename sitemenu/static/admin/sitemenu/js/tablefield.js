(function($){
    var tablefield_cnt = 0;
    var table_types_count = 3;

    function get_new_row(){
        return {
            //header: false,
            highlight: false,
            data: ['']
        };
    }

    $(function(){
        $('.j_tablefield').each(init_tablefield);

        $('.add-row a').click(function(){
            var add_row = $(this).closest('tr');
            if(add_row.length === 0){
                add_row = $(this).parent();
            }
            if(add_row.length !== 0){
                var textarea = add_row.prev().prev().find('.j_tablefield');
                if(textarea.length > 0){
                    textarea.each(init_tablefield);
                }
            }
        });
    });

    function init_tablefield(){

        var textarea = $(this);

        tablefield_cnt++;

        $('.tf_main_container', textarea.parent()).remove();

        textarea.hide();

        var data = null;
        if (textarea.val().length) {
            data = $.parseJSON(textarea.val());
        }

        if(data === null){
            data = {
                width: 1,
                height: 1,
                table_type: 0,
                rows: [
                    get_new_row()
                ]
            };
        }

        var container = $('<div class="tf_main_container"></div>');
        var table_container = $('<div></div>');
        var table_control = $('<div class="tf_table_control"></div>');
        var table_width_input = $('<input class="tf_small_input tf_hw_input" value="' + data.width + '" type="text">');
        var table_height_input = $('<input class="tf_small_input tf_hw_input" value="' + data.height + '" type="text">');
        table_control.append(table_width_input);
        table_control.append('x');
        table_control.append(table_height_input);

        container.append(table_control);

        var table_type = $('<div class="tf_table_type_container"></div>');

        for(var i=0; i<table_types_count; i++){
            var div = $('<div class="tf_table_type_subcontainer"></div>');
            input = $('<input value="' + i + '" class="tf_table_type_input" name="tf_table_type_' + tablefield_cnt + '" type="radio">');
            if(data.table_type == i){
                input.attr('checked', true);
            }
            input.change(set_table_type);
            div.append(input);
            div.append($('<span class="tf_table_type tf_table_type_'+i+'"></span>'));
            table_type.append(div);
        }

        container.append(table_type);

        container.append($('<div class="clear"></div>'));

        container.append(table_container);

        textarea.after(container);

        rebuild_table();

        table_width_input.change(rebuild_table);
        table_height_input.change(rebuild_table);



        // $('input.tf_hw_input', container).change(rebuild_table);
        // $('input.tf_table_type_input', container).change(set_table_type);


        function rebuild_table(){
            var new_width = parseInt(table_width_input.val(), 10);
            var new_height = parseInt(table_height_input.val(), 10);

            if(!isNaN(new_width) && !isNaN(new_height)){
                data.width = new_width;
                data.height = new_height;
            }
            table_width_input.val(data.width);
            table_height_input.val(data.height);
            for(var i=0; i<data.height; i++){
                if(typeof(data.rows[i]) == 'undefined'){
                    data.rows[i] = get_new_row();
                }
                for(var j=0; j<data.width; j++){
                    if(typeof(data.rows[i].data[j]) == 'undefined'){
                        data.rows[i].data[j] = '';
                    }
                }
            }
            render_table();
            save_table_to_field();
        }

        function render_table(){
            var table = $('<table></table>');
            table.addClass('tf_selected_table_type_'+data.table_type);
            for(var i=0; i<data.height; i++){
                var tr = $('<tr></tr>');
                table.append(tr);
                if(data.rows[i].highlight){
                    tr.addClass('tf_highlited_row');
                }
                if(i === 0){
                    tr.addClass('tf_first_row');
                }
                var th = $('<th></th>');
                tr.append(th);
                var checkbox = $('<input type="checkbox" class="tf_table_input_hl">');
                checkbox.data('i', i);
                checkbox.attr('checked', data.rows[i].highlight);
                th.append(checkbox);
                row = data.rows[i];
                for(var j=0; j<data.width; j++){
                    var td = $('<td></td>');
                    tr.append(td);
                    if(j === 0){
                        td.addClass('tf_first_column');
                    }
                    var input = $('<input class="tf_table_input" type="text" value="' + data.rows[i].data[j] + '" />');
                    input.data('i', i);
                    input.data('j', j);
                    td.append(input);
                }

                var td = $('<td></td>');
                tr.append(td);
                td.addClass('tf_actions');

                actions = $('<a href="#" class="j_tf_action_up tf_action_up">&uarr;</a><a href="#" class="j_tf_action_down tf_action_down">&darr;</a>');
                // <a href="#" class="j_tf_action_remove tf_action_remove">&times;</a>
                td.append(actions);

            }

            $('input.tf_table_input', table).change(function() {
                set_value($(this));
            });

            $('input.tf_table_input_hl', table).change(set_highlight);

            table_container.html(table);

            $('.j_tf_action_up').click(tr_to_up);
            $('.j_tf_action_down').click(tr_to_down);
        }

       function tr_to_up(event) {
            current_tr = $(this).closest('tr');
            prev_tr = current_tr.prev('tr');

            if(prev_tr.length > 0) {
                $('td input', current_tr).each(function( index, value ) {

                  current_input = $(value);
                  prev_input = $('td:eq('+index+') input', prev_tr);

                  current_input_val = current_input.val();

                  current_input.val(prev_input.val());
                  prev_input.val(current_input_val);

                  set_value(current_input);
                  set_value(prev_input);

                });
            }
            event.stopImmediatePropagation();
            return false;
        }

        function tr_to_down(event) {
            current_tr = $(this).closest('tr');
            next_tr = current_tr.next('tr');


            if(next_tr.length > 0) {
                $('td input', current_tr).each(function( index, value ) {

                  current_input = $(value);
                  next_input = $('td:eq('+index+') input', next_tr);

                  current_input_val = current_input.val();

                  current_input.val(next_input.val());
                  next_input.val(current_input_val);

                  set_value(current_input);
                  set_value(next_input);

                });
            }
            event.stopImmediatePropagation();
            return false;
        }

        function set_value(input){
            // var input = $(this);
            var ii = parseInt(input.data('i'), 10);
            var ij = parseInt(input.data('j'), 10);
            if(!isNaN(ii) && !isNaN(ij)){
                data.rows[ii].data[ij] = input.val();
                save_table_to_field();
            }
        }

        function set_highlight(){
            var input = $(this);
            var ii = parseInt(input.data('i'), 10);
            if(!isNaN(ii)){
                data.rows[ii].highlight = input.attr('checked');
                save_table_to_field();
                render_table();
            }
        }

        function set_table_type(){
            var input = $(this);
            var ttype = parseInt(input.val(), 10);
            if(!isNaN(ttype)){
                data.table_type = ttype;
                save_table_to_field();
                render_table();
            }
        }

        function save_table_to_field(){
            console.log(data);
            if((data.width > 1 && data.height > 0) || (data.width > 0 && data.height > 1)){
                textarea.val(JSON.stringify(data));
            } else {
                textarea.val('');
            }
        }

    }



})(django.jQuery);
