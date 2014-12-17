
define(['d3'], function(d3){
    var formatNumber = d3.format(",.2f");

    var InfoConverter = {
        convert: function(label, field, values){
            return {
                label: label,
                total: formatNumber(d3.sum(values, function(d){ return d[field]; })),
                deviation: formatNumber(d3.deviation(values, function(d){ return d[field] || 0; })),
            }
        }
    };

    return {
        modify: function(data){
            return {
                startDate: new Date(data.info.start_date),
                endDate: new Date(data.info.end_date),
                infocards: [
                    InfoConverter.convert('POINTS', 'points', data.values),
                    InfoConverter.convert('DISTANCE', 'distance', data.values),
                    InfoConverter.convert('DURATION', 'duration', data.values),
                ]
            }
        }
    };
});
