jQuery(document).ready(function () {
    jQuery("input[name=group]").autocomplete({
        source: function (request, response) {
            jQuery.ajax({
                url: "/laf/ajax/get_groups/" + request.term,
                dataType: "json",
                success: function (data) {
                    var results = new Array();
                    for (key in data) {
                        results.push(data[key].name);
                    }
                    return response(results);
                }
            });
        }
    });
});