define(function (require) {
    var $ = require('jquery'),
        crossfilter = require('crossfilter'),
        chart = require('./controller/dynamicchart'),
        Feed = require('./controller/activityfeed'),
        DataProvider = require('./providers/activity'),
        InfoModifier = require('./modifiers/infomodifier');


    function Demo(elt){
        this.$elt = $(elt);
    };

    Demo.prototype = {
        init: function(){
        },

        update: function(data){

            var margin = {left: 40, right: 50, paddingLeft: 95};

            data.values.forEach(function(d, i) {
                d.index = i;
                d.date = new Date(d.datetime);
            });

            var activities = crossfilter(data.values),
                all = activities.groupAll(),
                date = activities.dimension(function(d) { return d.date; }),
                dates = date.group(d3.time.day);

            var info = InfoModifier.modify(data);

            var dc = chart()
                .dimension(date)
                .group(dates)
                .round(d3.time.day.round)
              .x(d3.time.scale()
                .domain([info.startDate, info.endDate])
                .rangeRound([40, this.$elt.width()-margin.paddingLeft]))
              .y(d3.scale.linear()
                .range([40, 0]));

            var elts = d3.selectAll('.js-dynamic-chart');
            dc(elts);

            var feed = new Feed('.js-dynamic-feed');

            function updateActivities(){
                var actByDate = d3.nest()
                    .key(function(d){ return d3.time.day(d.date); });
                var top40 = actByDate.entries(date.top(40));

                feed.render(top40);
            }

            dc.on('brush', updateActivities).on('brushend', updateActivities);
        }
    }

    return Demo;
});
