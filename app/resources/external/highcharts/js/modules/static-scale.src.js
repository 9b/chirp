/**
 * @license Highcharts JS v6.0.2 (2017-10-20)
 * StaticScale
 *
 * (c) 2016 Torstein Honsi, Lars A. V. Cabrera
 *
 * --- WORK IN PROGRESS ---
 *
 * License: www.highcharts.com/license
 */
'use strict';
(function(factory) {
    if (typeof module === 'object' && module.exports) {
        module.exports = factory;
    } else {
        factory(Highcharts);
    }
}(function(Highcharts) {
    (function(H) {
        /**
         * (c) 2017 Torstein Honsi, Lars Cabrera
         *
         * License: www.highcharts.com/license
         */

        var Chart = H.Chart,
            each = H.each,
            pick = H.pick;

        Chart.prototype.adjustHeight = function() {
            each(this.axes, function(axis) {
                var chart = axis.chart,
                    animate = !!chart.initiatedScale && chart.options.animation,
                    staticScale = axis.options.staticScale,
                    height,
                    diff;
                if (
                    H.isNumber(staticScale) &&
                    !axis.horiz &&
                    H.defined(axis.min)
                ) {
                    height = pick(
                        axis.unitLength,
                        axis.max + axis.tickInterval - axis.min
                    ) * staticScale;

                    // Minimum height is 1 x staticScale.
                    height = Math.max(height, staticScale);

                    diff = height - chart.plotHeight;

                    if (Math.abs(diff) >= 1) {
                        chart.plotHeight = height;
                        chart.setSize(null, chart.chartHeight + diff, animate);
                    }
                }

            });
            this.initiatedScale = true;
        };
        Chart.prototype.callbacks.push(function(chart) {
            H.addEvent(this, 'render', function() {
                chart.adjustHeight();
            });
        });

    }(Highcharts));
}));
