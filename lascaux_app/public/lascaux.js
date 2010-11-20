jQuery(document).ready(function () {
    var height = jQuery('.lascaux.debug-panel > .body').outerHeight();
    var panel = jQuery('.lascaux.debug-panel');
    jQuery(panel).find('.header').find('a').attr('href', '');
    jQuery(panel).find('.close').bind('click', function () {
        if (jQuery(panel).data('expanded')) {
            jQuery(panel).data('expanded', false);
            jQuery(panel).removeClass('expanded');
        } else {
            jQuery(panel).data('expanded', true);
            jQuery(panel).addClass('expanded');
        }
        return false;
    });
});
