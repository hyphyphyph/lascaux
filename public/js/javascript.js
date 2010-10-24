$(document).ready(function() {
    $('form:not(.submitted) input').clearonfocus();
    $('.datepicker').datepicker();
    map.init();
    characteristics.init();
});
