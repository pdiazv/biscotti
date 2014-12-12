
define(['d3'], function(d3){
    return {
        modify: function(data){
            var group = d3.nest()
                .key(function(d){ return d.datetime; })
                .rollup(function(d){
                    return d3.sum(d, function(g){ return g.points; });
                }).entries(data.values);

            return group.map(function(d, i){
                return { key: i, date: new Date(d.key), values: d.values  };
            });
        }
    };
});
