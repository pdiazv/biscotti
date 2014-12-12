
define(['d3'], function(d3){
    return {
        modify: function(data){
            return {
                startDate: new Date(data.info.start_date),
                endDate: new Date(data.info.end_date),
            }
        }
    };
});
