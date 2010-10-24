$(document).ready(function() {
    $('form:not(.submitted) input[type:not(submit)]').clearonfocus();
    $('.datepicker').datepicker();
    map.init();
    characteristics.init();
});
