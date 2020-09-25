$(function(){

    feather.replace();

    $('.datatabletable').DataTable();

    $('[data-toggle="tooltip"]').tooltip()

    $('.clickable-row').click(function(){
        var url = $(this).data("href")
        window.location = url

    })

    var opts = {
        lines: 13, // The number of lines to draw
        length: 20, // The length of each line
        width: 3, // The line thickness
        radius: 25, // The radius of the inner circle
        scale: 1, // Scales overall size of the spinner
        corners: 1, // Corner roundness (0..1)
        speed: 1, // Rounds per second
        rotate: 0, // The rotation offset
        animation: 'spinner-line-fade-quick', // The CSS animation name for the lines
        direction: 1, // 1: clockwise, -1: counterclockwise
        color: 'blue', // CSS color or array of colors
        fadeColor: 'transparent', // CSS color or array of colors
        top: '50%', // Top position relative to parent
        left: '50%', // Left position relative to parent
        shadow: '0 0 1px transparent', // Box-shadow for the lines
        zIndex: 2000000000, // The z-index (defaults to 2e9)
        className: 'spinner', // The CSS class to assign to the spinner
        position: 'absolute', // Element positioning
    };

    $('.btn, a').click(function(){
        var target = document.getElementById('spinner');
        var spinner = new Spinner(opts).spin(target);
        $('.modal').on('shown.bs.modal', function (e) {
            spinner.stop()
          })
    })


});
