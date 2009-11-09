$(document).ready(function(){
    $(".cktxt").each(function() {
        var cb = $(this),
            textbox_id = cb.attr("id").slice(0, -3),
            textbox = $("#" + textbox_id);

        cb.change(function() {
            if(cb.attr("checked")) {
                textbox.show();
            } else {
                textbox.hide();
            }
        }).change();
    });
});
