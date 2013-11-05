$(function(){
    var feedback_form_container = $(".j_feedback_form_container");
    if(feedback_form_container.length){
        $(feedback_form_container, '.j_feedback_form').on('submit', function(e){
            e.preventDefault();
            var feedback_form = $('.j_feedback_form');
            $(feedback_form).find('input[type=submit]').attr('disabled', 'disabled');
            post_data = feedback_form.serialize()+"&feedbackformsubmit=true";
            $.post(feedback_form.attr("action"), post_data, function( data ) {
                feedback_form_container.html( data );
            });
        });
    }
});
