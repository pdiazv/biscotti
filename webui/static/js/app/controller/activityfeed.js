define(['d3'], function(d3){

    var formatNumber = d3.format(",d"),
      formatChange = d3.format("+,d"),
      formatDate = d3.time.format("%B %d, %Y"),
      formatTime = d3.time.format("%I:%M %p");

    var ActivityFeed = function(selector){
        this.selector = selector;
    };

    ActivityFeed.prototype.render = function(activities){
        var date = d3.select(this.selector).selectAll(".date")
          .data(activities, function(d) { return d.key; });

        date.enter().append("div")
          .attr("class", "date")
          .append("h2")
              .attr("class", "day")
              .text(function(d) { return formatDate(d.values[0].date); });

        date.exit().remove();

        var activity = date.order().selectAll(".js-activity")
          .data(function(d) { return d.values; }, function(d) { return d.index; });

        var activityEnter = activity.enter().append("tr")
          .attr("class", "js-activity");

        activityEnter.append("td")
          .attr("class", "time")
          .text(function(d) { return formatDate(d.date); });

        activityEnter.append("td")
          .attr("class", "type")
          .text(function(d) { return d.type; });

        activityEnter.append("td")
          .attr("class", "source")
          .text(function(d) { return d.source; });

        activityEnter.append("td")
          .attr("class", "distance")
          .text(function(d) { return formatNumber(d.distance) + " mi."; });

        activityEnter.append("td")
          .attr("class", "points")
          .classed("achiever", function(d) { return d.points > 100; })
          .text(function(d) { return d.points; });

        activity.exit().remove();

        activity.order();
    };

    return ActivityFeed;

});
