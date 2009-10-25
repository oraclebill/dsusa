$(function(){
	$('#wizard_content :input:visible').focus(function(){
		var img = MEDIA_URL + 'wizard/'+STEP+'/';
		
		img += this.name
		
		var tag_type = $(this).attr('type')
		if (tag_type == 'radio') {
			img += '_' + $(this).val()
		}
		img += '.png'

		var fs_id = get_fieldset_id(this)
		//console.info(img)
		$('img#fieldset_img_'+fs_id).attr('src', img)
	})
})
