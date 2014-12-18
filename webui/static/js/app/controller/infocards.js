define(['d3', 'handlebars'], function(d3, Handlebars){
    var hb = Handlebars;
    var cardTemplate = '{{#each cards}}\
    <div class="col-md-4 margin-top">\
      <div class="card stat-box">\
        <h1>{{total}}<small class="ui-stat-change positive">{{deviation}}%</small></h1>\
        <h3 class="ui-stat-unit">{{label}}</h3>\
      </div>\
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
