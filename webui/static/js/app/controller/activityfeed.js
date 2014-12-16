define(['d3'], function(d3){

    var formatNumber = d3.format(",.2f"),
      formatChange = d3.format("+,d"),
      formatDate = d3.time.format("%B %d, %Y"),
      formatTime = d3.time.format("%I:%M %p");

    var ActivityFeed = function(selector){
        this.selector = selector;
    };

    ActivityFeed.prototype.render = function(activities){
        var date = d3.select(this.selector).selectAll(".date")
          .data(activities, function(d) { return d.key; });

        var dateEnter = date.enter()
            .append("div")
              .attr("class", "card date");

        dateEnter.append("h2")
              .attr("class", "day")
              .text(function(d) { return formatDate(d.values[0].date); });
        dateEnter.append('table')
            .attr('class', 'table')
              .html(
                  '<thead>\
                    <tr>\
                      <th>Name</th>\
                      <th>Type</th>\
                      <th>Source</th>\
                      <th>Distance</th>\
                      <th>Points</th>\
                    </tr>\
                  </thead>')
              .append('tbody')
                .attr('class', 'js-data-container');

        date.exit().remove();

        var activity = date.selectAll('.js-data-container').order().selectAll(".js-activity")
          .data(function(d) { return d.values; }, function(d) { return d.index; });

        var activityEnter = activity.enter().append("tr")
          .attr("class", "js-activity");

        activityEnter.append("td")
          .attr("class", "employee")
          .text(function(d) { return d.user.name; });

        activityEnter.append("td")
          .attr("class", "type")
          .text(function(d) { return d.type; });

        activityEnter.append("td")
          .attr("class", "source")
          .text(function(d) { return d.source; });

        activityEnter.append("td")
          .attr("class", "distance")
          .text(function(d) {
              return formatNumber(d.distance) + " mi."; });

        activityEnter.append("td")
          .attr("class", "points")
          .classed("achiever", function(d) { return d.points > 100; })
          .text(function(d) {
              return formatNumber(d.points); });

        activity.exit().remove();

        activity.order();
    };

    return ActivityFeed;

});
