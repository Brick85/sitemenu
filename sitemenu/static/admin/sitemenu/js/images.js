(function($){
    $(function(){
        $('p.file-upload a').each(function(){
            img = $(this).attr('href');
            if(endsWith(img, 'jpg') || endsWith(img, 'jpeg') || endsWith(img, 'png')){
                $(this).addClass('image_popup');
                $(this).html('<img src="'+img+'" class="preview_image_small" /><div class="preview_image"><img src="'+img+'" /></div>');
            }
        });
        $('p.file-upload a.image_popup').click(function(){
            $('div.preview_image', this).toggle();
            return false;
        });
    });
    function endsWith(str, suffix) {
        return str.toLowerCase().indexOf(suffix, str.length - suffix.length) !== -1;
    }
})(django.jQuery);
