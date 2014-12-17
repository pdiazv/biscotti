define(['d3', 'handlebars'], function(d3, Handlebars){
    var hb = Handlebars;
    var cardTemplate = '{{#each cards}}\
    <div class="col-md-3 ui-stat">\
        <div class="ui-stat-value">{{total}}<span class="ui-stat-change positive">{{deviation}}%</span></div>\
        <div class="ui-stat-unit">{{label}}</div>\
    </div>\
    {{/each}}';

    var InfoCards = function($elt){
        this.$elt = $elt.find('.js-stats');
    };

    InfoCards.prototype.render = function(data){
        var template = hb.compile(cardTemplate);
        var html     = template({ cards: data.infocards });

        this.$elt.html(html);
    };


    return InfoCards;
})
