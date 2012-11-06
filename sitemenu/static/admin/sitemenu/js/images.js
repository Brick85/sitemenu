(function($){
    $(function(){
        $('p.file-upload a').each(function(){
            img = $(this).attr('href');
            $(this).html('<img src="'+img+'" class="preview_image_small" /><div class="preview_image"><img src="'+img+'" /></div>');
        });
        $('p.file-upload a').click(function(){
            $('div.preview_image', this).toggle();
            return false;
        });
    });
})(django.jQuery);
