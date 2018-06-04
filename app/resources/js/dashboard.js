$( document ).ready(function() {

    $.getJSON('/data/article-by-day-30', function(data) {
        Highcharts.chart('content-by-day-30', {
            chart: {
                type: 'column'
            },
            legend: {
                enabled: false
            },
            title: {
                text: '30-day Ingested Content'
            },
            xAxis: {
                categories: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
            },
            yAxis: {
                title: {
                    text: 'Unique Content'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
            series: [{
                name: 'Content',
                data: data
            }]
        });
    });

    $.getJSON('/data/article-tag-cloud', function(data) {
        Highcharts.chart('article-tag-cloud', {
            title: {
                text: 'Article Top 25 Tags'
            },
            series: [{
                type: 'wordcloud',
                data: data,
                name: 'Tag'
            }]
        });
    });

    $.getJSON('/data/article-sources', function(data) {
        var thead_row = $('<tr></tr>')
                        .append($('<th></th>').text('Source'))
                        .append($('<th></th>').text('Rank'));
        var thead = $('<thead></thead>')
                    .addClass('thead-dark')
                    .append(thead_row);
        var tbody = $('<tbody></tbody>');
        for (var i=0; i < data.length; i++) {
            tbody.append($('<tr></tr>')
                        .append($('<td></td>').text(data[i][0]))
                        .append($('<td></td>').text(data[i][1])));
        }
        var table = $('<table></table>')
                    .addClass('table')
                    .append(thead)
                    .append(tbody);
        $('#source-distribution').html(table);
    });

    $.getJSON('/data/count-by-monitor-by-day-30', function(data) {
        Highcharts.chart('monitor-heatmap', {
            chart: {
                type: 'heatmap',
                plotBorderWidth: 1
            },
            title: {
                text: 'Monitor Content By Day'
            },
            xAxis: {
                categories: data.series
            },
            yAxis: {
                categories: ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                             'Friday', 'Saturday', 'Sunday'],
                title: null
            },

            colorAxis: {
                min: 0,
                minColor: '#FFFFFF',
                maxColor: Highcharts.getOptions().colors[0]
            },

            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.xAxis.categories[this.point.x] + '</b> published <br><b>' +
                        this.point.value + '</b> content on <br><b>' + this.series.yAxis.categories[this.point.y] + '</b>';
                }
            },

            legend: {
                align: 'right',
                layout: 'vertical',
                margin: 0,
                verticalAlign: 'top',
                y: 25,
                symbolHeight: 280
            },

            series: [{
                name: 'Content',
                borderWidth: 1,
                data: data.data,
                dataLabels: {
                    enabled: true,
                    color: '#000000'
                }
            }]
        });
    });

});