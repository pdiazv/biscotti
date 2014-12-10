

(function(){

function LoadDemo(){

    $.get('/stats_data', function(data){
        data.forEach(function(d, i){
            d.index = i;
            d.date = new Date(d.datetime);
        });


        new DemoChart()
            .Init()
            .Render(data);
    });


}




function DemoChart(){

    var self = this;

    this.Init = function(){
        var margin = {top: 20, right: 20, bottom: 30, left: 40};
        self.width = 960 - margin.left - margin.right;
        self.height = 500 - margin.top - margin.bottom;

        self.x = d3.time.scale()
            .domain([new Date(2014, 11, 1), new Date(2014, 11, 30)])
            .rangeRound([0, width]);

        self.y = d3.scale.linear()
            .range([height, 0]);

        self.xAxis = d3.svg.axis()
            .scale(self.x)
            .ticks(d3.time.day)
            .orient("bottom");

        self.yAxis = d3.svg.axis()
            .scale(self.y)
            .orient("left")
            .tickSize(self.width);

        self.svg = d3.select(".js-chart-container").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        return self;
    }

    this.Render = function(data){
        //self.x.domain(data.map(function(d) { return d.letter; }));
        self.y.domain([0, d3.max(data, function(d) { return d.points; })]);

        svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

        svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("Frequency");

        svg.selectAll(".bar")
          .data(data)
        .enter().append("rect")
          .attr("class", "bar")
          .attr("x", function(d) { return x(d.letter); })
          .attr("width", x.rangeBand())
          .attr("y", function(d) { return y(d.frequency); })
          .attr("height", function(d) { return height - y(d.frequency); });

        return self;
    }
}

}())
