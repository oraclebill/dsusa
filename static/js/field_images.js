$(function(){
	/** 
	 * Defines a function to set the display image based on selected field.
	 * Works for text and radio input elements (select?)
	 * 
	 * Image to display -> 
	 *     <MEDIA_URL>/wizard/<step_name_slug>/<field_name>['_' + <option_number>].png
	 *     
	 * @param {Object} element
	 */
    function set_image(element) {		
		var img = MEDIA_URL + 'wizard/'+STEP+'/';

		img += this.name;  // field name

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
