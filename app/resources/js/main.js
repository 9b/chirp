$( document ).ready(function() {
    console.log("Ready for JS!");

    function read_time_class(read_time) {
        if (read_time <= 5) {
            return "FAST";
        } else if (read_time > 5 && read_time < 10) {
            return "MEDIUM";
        } else {
            return "SLOW";
        }
    }

    function title(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    // $('#accordion').on('hidden.bs.collapse', function () {
    //     $('.article-link').removeClass('article-link-fade');
    //     $('a[aria-expanded="false"]').addClass('article-link-fade');
    // });

    $('.left-card').click(function() {
        $this = $(this);
        $('.article-highlight').removeClass('article-highlight');
        $this.addClass('article-highlight');
        $.ajax({
            url: '/monitors?id=' + $this.attr('ref'),
            type: 'get',
            dataType: 'json',
            contentType:'application/json',
            success: function(data) {
                if (data.success) {
                    $('#accordion').empty();
                    $container = $('#accordion');

                    for (var i=0; i < data.articles.length; i++) {
                        var a = data.articles[i];
                        var random = Math.random().toString(36).substring(7);
                        var pull_link = '<a class="pull-right" target="_blank" href="' + a.href + '"><i class="fa fa-link"></i></a>';
                        var slug = "link-" + random;
                        var card_link = '<a class="article-link" href="#" data-toggle="collapse" data-target="' + '#' + slug + '" aria-expanded="false" aria-controls="' + slug + '">' + '[' + a.date + '] ' + a.title + '</a>';

                        var body_footer = '<span class="article-footer">';
                        body_footer += '<b><a href="' + a.source + '">' + a.source + '</a></b>';
                        body_footer += ' | ' + a.sentiment;
                        body_footer += ' | ' + a.word_count;
                        body_footer += ' | ';
                        for (var j=0; j < a.tags.length; j++) {
                            body_footer += '<span class="badge badge-secondary article-tag">' + title(a.tags[j]) + '</span> ';
                        }
                        body_footer += ' | ';

                        var text = "Chirp Alert: " + a.title;
                        var social = ['facebook', 'twitter', 'pinterest', 'email'];
                        for (var s=0; s < social.length; s++) {
                            button = build_social_button(social[s], a.href, text);
                            body_footer += button.prop('outerHTML');
                        }

                        body_footer += '</span>';

                        var card_body = $('<div></div>')
                                        .addClass('card-body')
                                        .append($('<p></p')
                                                .append($.parseHTML(a.summary))
                                        )
                                        .append($.parseHTML(body_footer));

                        var card_bottom = $('<div></div>')
                                          .attr({'id': 'link-' + random})
                                          .addClass('collapse')
                                          .addClass('card-bottom')
                                          .attr({'data-parent': '#accordion'})
                                          .append(card_body);

                        var card = $('<div></div>')
                                   .addClass('card')
                                   .append($('<div></div>')
                                           .addClass('card-header')
                                           .addClass(read_time_class(a.read_time).toLowerCase())
                                           .attr({'id': 'heading-' + random})
                                           .append($.parseHTML(card_link))
                                           .append($.parseHTML(pull_link))
                                    )
                                   .append(card_bottom);

                        $container.append(card);
                    }
                    $('.collapse').collapse();
                    // $('a[aria-expanded="false"]').addClass('article-link-fade');
                }
            }
        });
    })
});


/**

  <div class="card">
    <div class="card-header" id="headingOne">
      <a href="#" data-toggle="collapse" data-target="#collapseOne">Hello</a>
    </div>

    <div id="collapseOne" class="collapse"data-parent="#accordion">
      <div class="card-body">
        <p>hello</p>
      </div>
    </div>
  </div>


    <div class="card">
        <div class="card-header" id="heading-w5b1m">
            <a href="#" data-toggle="collapse" data-target="link-w5b1m" class="" aria-expanded="true">Report: Chinese government is behind a decade of hacks on software companies</a>
        </div>
        <div id="link-w5b1m" class="collapse show" data-parent="#accordion" style="">
            <div class="card-body">
                <p>Researchers from 401TRG, the threat research and analysis team at security company &lt;b&gt;ProtectWise&lt;/b&gt;, based the attribution on common network&amp;nbsp;...</p>
            </div>
        </div>
    </div>
 */