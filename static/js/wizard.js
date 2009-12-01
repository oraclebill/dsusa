var KEY_TAB = 9;

function wizard_go_to(step) {
	$('#next_step').val(step)
	$('form#wizard_form').submit();
}

function get_fieldset_id(element) {
	var id = false;
	$(element).parents().each(function(){
		if (this.tagName == 'FIELDSET') {
			id = $(this).attr('id').replace('fields_', '')
			return false
		}
	})
	return id;
}

$(function(){
	//Tabs navigation:	
	$('#wizard_content :input:visible:first').keydown(function(event){
		if (event.keyCode == KEY_TAB && event.shiftKey) {
			if (!IS_FIRST_STEP)
				wizard_go_to('_prev_')
			return false;
		}
	}).focus()
	$('#wizard_content :input:visible:last').keydown(function(event){
		if (event.keyCode == KEY_TAB && !event.shiftKey) {
			wizard_go_to('_next_')
			return false;
		}
	})
	$('#wizard_steps a').click(function(){
		wizard_go_to($(this).attr('step'))
		return false;
	})

	//Collapse fieldsets:
	$('fieldset.collapse legend').click(function() {
		$(this).parent().find('div').toggle('fast');
	})
})
