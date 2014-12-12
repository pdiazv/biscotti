

(function(){

function LoadDemo(){

    $.get('/stats_data', function(result){

        result.info.start_date = new Date(result.info.start_date);
        result.info.end_date = new Date(result.info.end_date);

        result.data.forEach(function(d, i){
            d.date = new Date(d.datetime);
        });

        var group = d3.nest()
            .key(function(d){ return d.datetime; })
            .rollup(function(d){
                return d3.sum(d, function(g){ return g.points; });
            }).entries(result.data);

        var groupData = group.map(function(d, i){
            return { key: i, date: new Date(d.key), values: d.values  };
        });

        new DemoChart()
            .Init(result.info)
            .Render(groupData);
    });


}




function DemoChart(){

    var self = this;

    this.Init = function(info){
        var $cont = $('.js-chart-container');
        var margin = {top: 20, right: 20, bottom: 30, left: 40},
            width = $cont.width() - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

        self.height = height;
        self.x = d3.time.scale()
            .domain([info.start_date, info.end_date])
            .rangeRound([margin.left, width]);

        self.y = d3.scale.linear()
            .range([height, 0]);

        self.xAxis = d3.svg.axis()
            .scale(self.x)
            .ticks(d3.time.day)
            .tickFormat(function(d){
                return d3.time.format('%a')(d)[0]; })
            .orient("bottom");

        self.weekAxis = d3.svg.axis()
            .scale(self.x)
            .ticks(d3.time.week)
            .orient("bottom");

        self.yAxis = d3.svg.axis()
            .scale(self.y)
            .ticks(7)
            .orient("right")
            .tickSize(width);

        self.svg = d3.select(".js-chart-container").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        self.weekSvg = d3.select(".js-chart-container").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", 100)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        return self;
    }

    this.Render = function(data){
        //self.x.domain(data.map(function(d) { return d.letter; }));
        self.y.domain([0, d3.max(data, function(d) { return d.values+100; })]);

        self.svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + self.height + ")")
              .call(self.xAxis);

        self.weekSvg.append("g")
              .attr("class", "week axis")
              .attr("transform", "translate(0, 0)")
              .call(self.weekAxis);

        var gy = self.svg.append("g")
              .attr("class", "y axis")
              .call(self.yAxis);

        gy.selectAll('g')
            .classed('minor', true);
        gy.selectAll('text')
            .attr('x', -40)
            .attr('dy', 4);

        self.svg.selectAll(".bar")
              .data(data)
            .enter().append("rect")
              .attr("class", "bar")
              .classed('ui-over-goal', function(d){ return d.values >= 1000; })
              .attr("x", function(d) {
                  return self.x(d.date); })
              .attr("width", 30)
              .attr("y", function(d) {
                  return self.y(d.values); })
              .attr("height", function(d) {
                  return self.height - self.y(d.values); });

        return self;
    }
}


LoadDemo();

}())
