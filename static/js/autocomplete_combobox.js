(function($) {
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
                return $("#" + id);
            }
            choices = default_choices;
        }

        $$.replaceWith(select_html(id, name, val, choices, default_choices));
        $$ = $("#" + id);

        function clear_error(item) {
            $(item).parent().parent().removeClass("invalid").find("ul").remove();
        }

        if (val && $.inArray(val, choices) == -1) {
            $$.parent().parent().addClass("invalid").removeClass("valid");
            $$.before(
                '<ul class="errorlist" style="display: block;"><li>'+
                    val +
                    ' is invalid now. Choose something else</li></ul>'
            );
            $$.change(clear_error);
        } else {
            clear_error($$);
        }
        return $$;
    };
})(jQuery);