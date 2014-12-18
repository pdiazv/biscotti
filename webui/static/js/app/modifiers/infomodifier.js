
define(['d3'], function(d3){
    var formatNumber = d3.format(",.2f");
    var toSeconds = function(v) {
        return v.substring(0,2) * 3600 +
            v.substring(3,5) * 60 +
            v.substring(6,8);
    };

    var secondsToString = function(s){
        var h = (s / 3600) | 0;
        return d3.format(',.d')(h);
    }

    var NumberConverter = {
        convert: function(label, field, values){
            return {
                label: label,
                total: formatNumber(d3.sum(values, function(d){ return d[field]; })),
                deviation: formatNumber(d3.deviation(values, function(d){ return d[field] || 0; })),
            }
        }
    };

    var TimeConverter = {
        convert: function(label, field, values){
            return {
                label: label,
                total: secondsToString(d3.sum(values, function(d){ return toSeconds(d[field]); })),
                deviation: 0,
            }
        }
    };

    return {
        modify: function(data){
            return {
                goal: data.info.goal,
                startDate: new Date(data.info.start_date),
                endDate: new Date(data.info.end_date),
                infocards: [
                    NumberConverter.convert('POINTS', 'points', data.values),
                    NumberConverter.convert('DISTANCE', 'distance', data.values),
                    TimeConverter.convert('DURATION', 'duration', data.values),
                ]
            }
        }
    };
});
