$( document ).ready(function() {
    $('.monitor-action').click(function() {
        var $this = $(this);
        var hash = $(this).attr('term-id');
        var action = $(this).attr('action');

        $.ajax({
            type: 'GET',
            url: '/monitor/' + hash + "?action=" + action,
            success: function(data) {
                if (data.success) {
                    $this.parents("tr").remove();
                }
            }
        });
    });
});