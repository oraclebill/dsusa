(function($) {
	// function select_html(id, name, value, choices, default_choices) {
	// 	var options = '<option value="">---------</option>',
    //         selected = '',
    //         option_value = '',
    //         option_text = '';

	// 	for (var i=0; i<choices.length; i++) {
    //         option_text = choices[i];
    //         if (default_choices && option_text.toLowerCase() in default_choices) {
    //             option_value = default_choices[option_text.toLowerCase()].value;
    //         } else {
    //             option_value = option_text;
    //         }
    //         selected = value == option_value ? ' selected="selected"' : '';
	// 		options += '<option value="'+ option_value +'"'+selected+'> '+ option_text +'</option>';
	// 	}
	// 	return '<select name="'+name+'" id="'+id+'">'+options+'</select>';
	// }

	function select_html(id, name, value, choices) {
		var options = '',
            selected = '',
            option = '';

		for (var i=0; i<choices.length; i++) {
            option = choices[i];
            selected = value == option ? ' selected="selected"' : '';
			options += '<option value="'+ option +'"'+selected+'> '+ option +'</option>';
		}
		return '<select name="'+name+'" id="'+id+'">'+options+'</select>';
	}


	function input_html(id, name, value) {
		return '<input type="text" name="'+name+'" id="'+id+'" value="'+value+'">';
	}

    $.fn.update_choices = function(choices, default_selects) {
        var $$ = this,
            val = $$.val(),
            id = $$.attr('id'),
            name = $$.attr('name'),
            default_choices = (id in default_selects) ? default_selects[id] : null;

        if (!choices.length) {
            if (!default_choices) {
                $$.replaceWith(input_html(id, name, val));
                return;
            }
            choices = default_choices;
            // for (key in default_choices) {
            //     choices.push(default_choices[key].text);
            // }
            // console.log('default_choices', default_choices);
            // console.log(choices);
        }

        $$.replaceWith(select_html(id, name, val, choices, default_choices));
        $$ = $("#" + id);

        if (val && !$$.find("option[selected=selected]").length) {
            $$.css({background: "red"});
        }
    };
})(jQuery);