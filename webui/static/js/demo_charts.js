

(function(){

function LoadDemo(){

    $.get('/stats_data', function(result){
        result.data.forEach(function(d, i){
            d.index = i;
            d.date = new Date(d.datetime);
        });


        new DemoChart()
            .Init()
            .Render(result.data);
    });


}




function DemoChart(){

    var self = this;

    this.Init = function(){
        var $cont = $('.js-chart-container');
        var margin = {top: 20, right: 20, bottom: 30, left: 40},
            width = $cont.width() - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

        self.height = height;
        self.x = d3.time.scale()
            .domain([new Date(2014, 3, 1), new Date(2014, 3, 30)])
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
        self.y.domain([0, d3.max(data, function(d) { return d.points+100; })]);

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
              .classed('ui-over-goal', function(d){ return d.points >= 1000; })
              .attr("x", function(d) { return self.x(d.date) - 5; })
              .attr("width", 30)
              .attr("y", function(d) { return self.y(d.points); })
              .attr("height", function(d) { return self.height - self.y(d.points); });

        return self;
    }
}


LoadDemo();

}())
