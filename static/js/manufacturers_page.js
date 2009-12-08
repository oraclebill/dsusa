(function($) {
    $.fn.update_choices = (function(){
	    function select_html(id, name, value, choices) {
		    var options = '',
	            selected = '',
				option_selected = false,
	            option = '';

		    for (var i=0; i<choices.length; i++) {
                option = choices[i]; 
				if (value == option) {
					option_selected = true;
					selected = ' selected="selected"';
				}
				else {
					selected = '';
				}
			    options += '<option value="'+ option +'"'+selected+'> '+ option +'</option>';
		    }
			if (option_selected) {
				options = '<option value="" selected="selected">--------</option>' + options;			
			} else {
				options = '<option value="">--------</option>' + options;			
			}
			
		    return '<select name="'+name+'" id="'+id+'">'+options+'</select>';
	    }


	    function input_html(id, name, value) {
		    return '<input type="text" name="'+name+'" id="'+id+'" value="'+value+'">';
	    }

        return function(choices, default_selects) {
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
				$$.children('option:first').attr('selected','selected');
//                $$.before(
//                    '<ul class="errorlist" style="display: block;"><li>'+
//                        val +
//                        ' is invalid now. Choose something else</li></ul>'
//                );
                $$.change(clear_error);
            } else {
                clear_error($$);
            }
            return $$;
        };
    })();

    $.fn.manufacturerHandle = function(options) {
        var default_selects = options.default_selects;

        // prepare dictionry with options for default selects
        $("#wizard_form select").each(function() {
            var $$ = $(this);
            default_selects[$$.attr("id")] = $.map($$.find("option"), function(option) {
                return $(option).text();
            });
        });

        function material_change() {
            var dependent_inputs = [ "door_style", "finish_color", "finish_type", "finish_options"],
                material = $("#id_cabinet_material").val(),
                manufacturer_data = $("#id_manufacturer").data("json_data"),
                material_data = manufacturer_data ? manufacturer_data.material[material] : null,
                choices = null;

            $.each(dependent_inputs, function(i) {
                choices = material_data ? material_data[dependent_inputs[i]] : [];
                $("#id_" + dependent_inputs[i]).update_choices(choices, default_selects);
            });
    	    $('form').validation(options.validation_json);
        }

        function manufacturer_change() {
            var manufacturer_input = $("#id_manufacturer"),
            manufacturer_val = manufacturer_input.val();

            // this is to prevent change on both `result` and `change` events
            if (manufacturer_input.data("last_choice_update_on") == manufacturer_val) {
                return;
            }

            $.getJSON(options.manufacturer_ajax_url, {manufacturer: manufacturer_val},
                      function(data) {
                          manufacturer_input.data("json_data", "error" in data ? null : data);
                          if ("error" in data) {
                              $("#id_product_line").update_choices([], default_selects);
                              $("#id_cabinet_material").update_choices([], default_selects).change(material_change).change();
                          } else {
                              $("#id_product_line").update_choices(data.product_line, default_selects);
                              $("#id_cabinet_material").update_choices(data.materials_list, default_selects).change(material_change).change();
                          }
                      });
            manufacturer_input.data("last_choice_update_on", manufacturer_val);
        }

	    $(this).autocomplete(options.manufacturers).result(manufacturer_change).change(manufacturer_change);
        manufacturer_change();
    };

})(jQuery);