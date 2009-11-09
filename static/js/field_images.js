$(function(){
    function set_image(element) {
		var img = MEDIA_URL + 'wizard/'+STEP+'/';

		img += this.name;

		var tag_type = $(this).attr('type');
		if (tag_type == 'radio') {
			img += '_' + $(this).val();
		}
		img += '.png';

		var fs_id = get_fieldset_id(this);
		//console.info(img)
		$('img#fieldset_img_'+fs_id).attr('src', img);
    }
	$('#wizard_content input:visible').focus(set_image);
	$('#wizard_content input[type=radio]:visible, #wizard_content input[type=checkbox]:visible').change(function() {
        if ($(this).attr('checked')) {
            set_image(this);
        }
    });
});
