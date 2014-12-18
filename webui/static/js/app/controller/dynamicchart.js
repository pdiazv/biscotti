
define(['d3'], function(d3){

    return function() {
        var margin = {top: 5, right: 50, bottom: 20, left: 40},
            x,
            y,
            axis = d3.svg.axis().orient("bottom"),
            brush = d3.svg.brush(),
            brushDirty,
            dimension,
            group,
            round;

        axis.ticks(d3.time.day)
            .tickFormat(function(d){ return d3.time.format('%a')(d)[0]; });

        function chart(div) {
          var width = x.range()[1],
              height = y.range()[0];

          y.domain([0, getValue(group.top(1)[0].value)]);

          div.each(function() {
            var div = d3.select(this),
                g = div.select("g");

            // Create the skeletal chart.
            if (g.empty()) {

              g = div.append("svg")
                  .attr("width", width + margin.left + margin.right)
                  .attr("height", height + margin.top + margin.bottom)
                .append("g")
                  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

              g.append("clipPath")
                  .attr("id", "dc-clip")
                .append("rect")
                  .attr("width", width)
                  .attr("height", height);

              g.selectAll(".bar")
                  .data(["background", "foreground"])
                .enter().append("path")
                  .attr("class", function(d) { return d + " bar"; })
                  .datum(group.all());

              g.selectAll(".foreground.bar")
                  .attr("clip-path", "url(#dc-clip)");

              g.append("g")
                  .attr("class", "axis")
                  .attr("transform", "translate(0," + height + ")")
                  .call(axis);

              // Initialize the brush component with pretty resize handles.
              var gBrush = g.append("g").attr("class", "brush").call(brush);
              gBrush.selectAll("rect").attr("height", height);
              gBrush.selectAll(".resize").append("path").attr("d", resizePath);
            }

            // Only redraw the brush if set externally.
            if (brushDirty) {
              brushDirty = false;
              g.selectAll(".brush").call(brush);
              div.select(".title a").style("display", brush.empty() ? "none" : null);
              if (brush.empty()) {
                g.selectAll("#clip-" + id + " rect")
                    .attr("x", 0)
                    .attr("width", width);
              } else {
                var extent = brush.extent();
                g.selectAll("#clip-" + id + " rect")
                    .attr("x", x(extent[0]))
                    .attr("width", x(extent[1]) - x(extent[0]));
              }
            }

            g.selectAll(".bar").attr("d", barPath);
          });

          function getValue(value){
              return !!value.avg ? value.avg : value;
          }

          function barPath(groups) {
            var path = [],
                i = -1,
                n = groups.length,
                d;
            while (++i < n) {
              d = groups[i];
              var day = new Date(d.key);
              day.setHours(23);
              path.push("M", x(day), ",", height, "V", y(getValue(d.value)), "h9V", height);
            }
            return path.join("");
          }

          function resizePath(d) {
            var e = +(d == "e"),
                x = e ? 1 : -1,
                y = height / 3;
            return "M" + (.5 * x) + "," + y
                + "A6,6 0 0 " + e + " " + (6.5 * x) + "," + (y + 6)
                + "V" + (2 * y - 6)
                + "A6,6 0 0 " + e + " " + (.5 * x) + "," + (2 * y)
                + "Z"
                + "M" + (2.5 * x) + "," + (y + 8)
                + "V" + (2 * y - 8)
                + "M" + (4.5 * x) + "," + (y + 8)
                + "V" + (2 * y - 8);
          }
        }

        brush.on("brushstart.chart", function() {
          var div = d3.select(this.parentNode.parentNode.parentNode);
          div.select(".title a").style("display", null);
        });

        brush.on("brush.chart", function() {
          var g = d3.select(this.parentNode),
              extent = brush.extent();
          if (round) g.select(".brush")
              .call(brush.extent(extent = extent.map(round)))
            .selectAll(".resize")
              .style("display", null);
          g.select("#dc-clip rect")
              .attr("x", x(extent[0]))
              .attr("width", x(extent[1]) - x(extent[0]));
          dimension.filterRange(extent);
        });

        brush.on("brushend.chart", function() {
          if (brush.empty()) {
            var div = d3.select(this.parentNode.parentNode.parentNode);
            div.select(".title a").style("display", "none");
            div.select("#dc-clip rect").attr("x", null).attr("width", "100%");
            dimension.filterAll();
          }
        });

        chart.margin = function(_) {
          if (!arguments.length) return margin;
          margin = _;
          return chart;
        };

        chart.x = function(_) {
          if (!arguments.length) return x;
          x = _;
          axis.scale(x);
          brush.x(x);
          return chart;
        };

        chart.y = function(_) {
          if (!arguments.length) return y;
          y = _;
          return chart;
        };

        chart.dimension = function(_) {
          if (!arguments.length) return dimension;
          dimension = _;
          return chart;
        };

        chart.filter = function(_) {
          if (_) {
            brush.extent(_);
            dimension.filterRange(_);
          } else {
            brush.clear();
            dimension.filterAll();
          }
          brushDirty = true;
          return chart;
        };

        chart.group = function(_) {
          if (!arguments.length) return group;
          group = _;
          return chart;
        };

        chart.round = function(_) {
          if (!arguments.length) return round;
          round = _;
          return chart;
        };

        return d3.rebind(chart, brush, "on");
    };

});
