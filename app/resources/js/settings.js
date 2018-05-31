$( document ).ready(function() {
    $('.credential-test').click(function() {
        var $this = $(this);
        $(this).html('<img id="loader" class="" src="/resources/img/loading.gif"/>');

        $.ajax({
            type: 'GET',
            url: '/account/settings/test',
            success: function(data) {
                $this.html('Test');
                if (data.success) {
                    var html = "<strong>Authentication Successful!</strong>";
                    html += " A session file has been saved for reuse later.";
                    $('.alert-container').html(html);
                    $('#settings-alert').addClass('alert-success').show();
                } else {
                    var html = "<strong>Authentication Failed!</strong>";
                    html += " " + data.message;
                    $('.alert-container').html(html);
                    $('#settings-alert').addClass('alert-danger').show();
                }
                setTimeout(function(){ $('.alert').hide(); }, 3000);
            }
        });
    });
});