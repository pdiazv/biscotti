
define(['d3'], function(d3){

    function Chart(){}

    Chart.prototype = {

        init: function(info){
            var margin = {top: 20, right: 50, bottom: 30, left: 40},
                width = info.width - margin.left - margin.right,
                height = 500 - margin.top - margin.bottom;

            this.height = height;
            this.x = d3.time.scale()
                .rangeRound([margin.left, width]);

            this.y = d3.scale.linear()
                .range([height, 0]);

            this.xAxis = d3.svg.axis()
                .scale(this.x)
                .ticks(d3.time.day)
                .tickFormat(function(d){ return d3.time.format('%a')(d)[0]; })
                .orient("bottom");

            this.weekAxis = d3.svg.axis()
                .scale(this.x)
                .ticks(d3.time.week)
                .orient("bottom");

            this.yAxis = d3.svg.axis()
                .scale(this.y)
                .ticks(7)
                .orient("right")
                .tickSize(width);

            this.svg = d3.select(info.containerSelector).append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
              .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            this.weekSvg = d3.select(info.weeklySelector).append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", 100)
              .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            return this;
        },

        render: function(info, data){
            this.x.domain([info.startDate, info.endDate]);
            this.y.domain([0, d3.max(data, function(d) { return d.values+100; })]);

            this.svg.append("g")
                  .attr("class", "x axis")
                  .attr("transform", "translate(0," + this.height + ")")
                  .call(this.xAxis);

            this.weekSvg.append("g")
                  .attr("class", "week axis")
                  .attr("transform", "translate(0, 0)")
                  .call(this.weekAxis);

            var gy = this.svg.append("g")
                  .attr("class", "y axis")
                  .call(this.yAxis);

            gy.selectAll('g')
                .classed('minor', true);
            gy.selectAll('text')
                .attr('x', -40)
                .attr('dy', 4);

            var self = this;
            this.svg.selectAll(".bar")
                  .data(data)
                .enter().append("rect")
                  .attr("class", "bar")
                  .classed('ui-over-goal', function(d){ return d.values >= 1000; })
                  .attr("x", function(d) { return self.x(d.date); })
                  .attr("width", 30)
                  .attr("y", function(d) { return self.y(d.values); })
                  .attr("height", function(d) { return self.height - self.y(d.values); });

            return this;
        }
    };

    return Chart;
});
