function field_images_hover(GROUPS, PAGE_NAME, MEDIA_URL) {
	function _group(name) {
		for (var k = 0; k < GROUPS.length; k++)
			for (var i = 0; i < GROUPS[k].length; i++)
				if (GROUPS[k][i] == name)
					return GROUPS[k];
		alert('Field not found - ' + name);
	}

	function image_for(element) {
		var group = _group(element.name),
		    img_path = '';
		for (var i = 0; i < group.length; i++) {
			var value = false;
			if (element.name == group[i])
				value = $(element).val();
			else
				value = $("input[name='"+group[i]+"']:checked").val();
			if (img_path.length > 0)
				img_path += '_';
			img_path += value;
		}
		img_path = MEDIA_URL + 'wizard/' + PAGE_NAME + '/' + group[0] + '/' + img_path + '.png';
		return img_path;
	}


	function update_pic(input_el, temporary) {
		var fs_id = get_fieldset_id(input_el),
		    img = image_for(input_el),
		    $image = $('img#fieldset_img_'+fs_id);

		$image.attr('src', img);
		if (!temporary)
			$image.data('original', img);
	}

	function reset_img(id) {
		var $image = $('img#fieldset_img_'+id);
		$image.attr('src', $image.data('original'));
	}

	$('#wizard_content li label').hover(
			function(){
				update_pic($(this).find('input').get(0), true);
			},
			function(){
				var fs_id = get_fieldset_id($(this).get(0));
				reset_img(fs_id);
			}
	);

	$('#wizard_content input:radio:checked').each(function(){
		update_pic(this);
	});

	$('#wizard_content input:radio').click(function(){
		update_pic(this);
	});

    function text_set_image(element) {
		var img = MEDIA_URL + 'wizard/'+STEP+'/';

		img += this.name;

		var tag_type = $(this).attr('type');
		img += '.png';

		var fs_id = get_fieldset_id(this);
		$('img#fieldset_img_'+fs_id).attr('src', img);
    }

    function text_reset_image(element) {
		var fs_id = get_fieldset_id(element);
		reset_img(fs_id);
    }

	$('#wizard_content input[type=text]').hover(
        text_set_image,
        function(){
            if ($(this).hasClass('focused')) {
                return;
            }
            text_reset_image(this);
		}
    ).focus(
        function() {
            text_set_image(this);
            $(this).addClass('focused');
        }
    ).blur(function(){
        $(this).removeClass('focused');
        text_reset_image(this);
	});
};