// © 2018-Today Aktiv Software (http://www.aktivsoftware.com).
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
odoo.define('status_bar_clock.date_time', function (require){
"use strict";

    var datetime = null;
    var date = null;
    var ajax = require('web.ajax');

    var update = function (final_clock_format) {

        var pythonToJsFormats = {
            '%a': 'ddd',
            '%A': 'dddd',
            '%w': 'd',
            '%d': 'DD',
            '%b': 'MMM',
            '%B': 'MMMM',
            '%m': 'MM',
            '%y': 'YY',
            '%Y': 'YYYY',
            '%H': 'HH',
            '%I': 'hh',
            '%p': 'A',
            '%M': 'mm',
            '%S': 'ss',
            '%f': 'SSS',
            '%z': 'ZZ',
            '%Z': 'z',
            '%j': 'DDDD',
            '%U': 'ww',
            '%W': 'ww',
            '%c': 'ddd MMM DD HH:mm:ss YYYY',
            '%x': 'MM/DD/YYYY',
            '%X': 'HH:mm:ss',
            '%%': '%'
        };

        ajax.rpc("/web/get_datetime", {}).done(function(final_clock_format){
            var convertFormat = function(format) {
                var converted = format;
                for(var name in pythonToJsFormats) {
                    if (pythonToJsFormats.hasOwnProperty(name)) {
                        converted = converted.split(name).join(pythonToJsFormats[name]);
                    }
                }
                return converted;
            };
            var converted_format = convertFormat(final_clock_format);
            date = moment(new Date())
            datetime.html(date.format(converted_format));
        })
    };

    $(document).ready(function(){
        datetime = $('#display_date_time')
        update();
        setInterval(update, 1000);
    });

});
