$( document ).ready(function() {
    $('.monitor-action').click(function() {
        var hash = $(this).attr('term-id');
        var action = $(this).attr('action');

        $.ajax({
            type: 'GET',
            url: '/monitors/' + hash + "?action=" + action,
            success: function(data) {
                console.log('CW');
            }
        });
    });
});